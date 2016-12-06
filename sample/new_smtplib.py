#!/root/Python-3.5.2/python 
import sys
import os
import errno
import getopt
import time
import socket
import asyncore
import asynchat
import collections
from warnings import warn
from email._header_value_parser import get_addr_spec, get_angle_addr
import asynchat
import smtpd
import asyncore
import smtplib
import traceback
__version__ = 'Python SMTP proxy version 0.3'

class Devnull:
    def write(self, msg): pass
    def flush(self): pass

DEBUGSTREAM = Devnull()
NEWLINE = '\n'
COMMASPACE = ', '
DATA_SIZE_DEFAULT = 33554432

class SMTPChannel(asynchat.async_chat):
    COMMAND = 0
    DATA = 1

    command_size_limit = 512
    command_size_limits = collections.defaultdict(lambda x=command_size_limit: x)

    @property
    def max_command_size_limit(self):
        try:
            return max(self.command_size_limits.values())
        except ValueError:
            return self.command_size_limit

    def __init__(self, server, conn, addr, data_size_limit=DATA_SIZE_DEFAULT,
                 map=None, enable_SMTPUTF8=False, decode_data=None):
        asynchat.async_chat.__init__(self, conn, map=map)
        self.smtp_server = server
        self.conn = conn
        self.addr = addr
        self.x_forward = ""
        self.data_size_limit = data_size_limit
        self.enable_SMTPUTF8 = enable_SMTPUTF8
        if enable_SMTPUTF8:
            if decode_data:
                raise ValueError("decode_data and enable_SMTPUTF8 cannot"
                                 " be set to True at the same time")
            decode_data = False
        if decode_data is None:
            warn("The decode_data default of True will change to False in 3.6;"
                 " specify an explicit value for this keyword",
                 DeprecationWarning, 2)
            decode_data = True
        self._decode_data = decode_data
        if decode_data:
            self._emptystring = ''
            self._linesep = '\r\n'
            self._dotsep = '.'
            self._newline = NEWLINE
        else:
            self._emptystring = b''
            self._linesep = b'\r\n'
            self._dotsep = ord(b'.')
            self._newline = b'\n'
        self._set_rset_state()
        self.seen_greeting = ''
        self.extended_smtp = False
        self.command_size_limits.clear()
        self.fqdn = socket.getfqdn()
        try:
            self.peer = conn.getpeername()
        except OSError as err:
            # a race condition  may occur if the other end is closing
            # before we can get the peername
            self.close()
            if err.args[0] != errno.ENOTCONN:
                raise
            return
        print('Peer:', repr(self.peer), file=DEBUGSTREAM)
        self.push('220 %s %s' % (self.fqdn, __version__))

    def _set_post_data_state(self):
        """Reset state variables to their post-DATA state."""
        self.smtp_state = self.COMMAND
        self.mailfrom = None
        self.rcpttos = []
        self.require_SMTPUTF8 = False
        self.num_bytes = 0
        self.set_terminator(b'\r\n')

    def _set_rset_state(self):
        """Reset all state variables except the greeting."""
        self._set_post_data_state()
        self.received_data = ''
        self.received_lines = []


    # properties for backwards-compatibility
    @property
    def __server(self):
        warn("Access to __server attribute on SMTPChannel is deprecated, "
            "use 'smtp_server' instead", DeprecationWarning, 2)
        return self.smtp_server
    @__server.setter
    def __server(self, value):
        warn("Setting __server attribute on SMTPChannel is deprecated, "
            "set 'smtp_server' instead", DeprecationWarning, 2)
        self.smtp_server = value

    @property
    def __line(self):
        warn("Access to __line attribute on SMTPChannel is deprecated, "
            "use 'received_lines' instead", DeprecationWarning, 2)
        return self.received_lines
    @__line.setter
    def __line(self, value):
        warn("Setting __line attribute on SMTPChannel is deprecated, "
            "set 'received_lines' instead", DeprecationWarning, 2)
        self.received_lines = value

    @property
    def __state(self):
        warn("Access to __state attribute on SMTPChannel is deprecated, "
            "use 'smtp_state' instead", DeprecationWarning, 2)
        return self.smtp_state
    @__state.setter
    def __state(self, value):
        warn("Setting __state attribute on SMTPChannel is deprecated, "
            "set 'smtp_state' instead", DeprecationWarning, 2)
        self.smtp_state = value

    @property
    def __greeting(self):
        warn("Access to __greeting attribute on SMTPChannel is deprecated, "
            "use 'seen_greeting' instead", DeprecationWarning, 2)
        return self.seen_greeting
    @__greeting.setter
    def __greeting(self, value):
        warn("Setting __greeting attribute on SMTPChannel is deprecated, "
            "set 'seen_greeting' instead", DeprecationWarning, 2)
        self.seen_greeting = value

    @property
    def __mailfrom(self):
        warn("Access to __mailfrom attribute on SMTPChannel is deprecated, "
            "use 'mailfrom' instead", DeprecationWarning, 2)
        return self.mailfrom
    @__mailfrom.setter
    def __mailfrom(self, value):
        warn("Setting __mailfrom attribute on SMTPChannel is deprecated, "
            "set 'mailfrom' instead", DeprecationWarning, 2)
        self.mailfrom = value

    @property
    def __rcpttos(self):
        warn("Access to __rcpttos attribute on SMTPChannel is deprecated, "
            "use 'rcpttos' instead", DeprecationWarning, 2)
        return self.rcpttos
    @__rcpttos.setter
    def __rcpttos(self, value):
        warn("Setting __rcpttos attribute on SMTPChannel is deprecated, "
            "set 'rcpttos' instead", DeprecationWarning, 2)
        self.rcpttos = value

    @property
    def __data(self):
        warn("Access to __data attribute on SMTPChannel is deprecated, "
            "use 'received_data' instead", DeprecationWarning, 2)
        return self.received_data
    @__data.setter
    def __data(self, value):
        warn("Setting __data attribute on SMTPChannel is deprecated, "
            "set 'received_data' instead", DeprecationWarning, 2)
        self.received_data = value

    @property
    def __fqdn(self):
        warn("Access to __fqdn attribute on SMTPChannel is deprecated, "
            "use 'fqdn' instead", DeprecationWarning, 2)
        return self.fqdn
    @__fqdn.setter
    def __fqdn(self, value):
        warn("Setting __fqdn attribute on SMTPChannel is deprecated, "
            "set 'fqdn' instead", DeprecationWarning, 2)
        self.fqdn = value

    @property
    def __peer(self):
        warn("Access to __peer attribute on SMTPChannel is deprecated, "
            "use 'peer' instead", DeprecationWarning, 2)
        return self.peer
    @__peer.setter
    def __peer(self, value):
        warn("Setting __peer attribute on SMTPChannel is deprecated, "
            "set 'peer' instead", DeprecationWarning, 2)
        self.peer = value

    @property
    def __conn(self):
        warn("Access to __conn attribute on SMTPChannel is deprecated, "
            "use 'conn' instead", DeprecationWarning, 2)
        return self.conn
    @__conn.setter
    def __conn(self, value):
        warn("Setting __conn attribute on SMTPChannel is deprecated, "
            "set 'conn' instead", DeprecationWarning, 2)
        self.conn = value

    @property
    def __addr(self):
        warn("Access to __addr attribute on SMTPChannel is deprecated, "
            "use 'addr' instead", DeprecationWarning, 2)
        return self.addr
    @__addr.setter
    def __addr(self, value):
        warn("Setting __addr attribute on SMTPChannel is deprecated, "
            "set 'addr' instead", DeprecationWarning, 2)
        self.addr = value

    # Overrides base class for convenience.
    def push(self, msg):
        asynchat.async_chat.push(self, bytes(
            msg + '\r\n', 'utf-8' if self.require_SMTPUTF8 else 'ascii'))

    # Implementation of base class abstract method
    def collect_incoming_data(self, data):
        limit = None
        if self.smtp_state == self.COMMAND:
            limit = self.max_command_size_limit
        elif self.smtp_state == self.DATA:
            limit = self.data_size_limit
        if limit and self.num_bytes > limit:
            return
        elif limit:
            self.num_bytes += len(data)
        if self._decode_data:
            self.received_lines.append(str(data, 'utf-8'))
        else:
            self.received_lines.append(data)

    # Implementation of base class abstract method
    def found_terminator(self):
        line = self._emptystring.join(self.received_lines)
        print('Data:', repr(line), file=DEBUGSTREAM)
        self.received_lines = []
        if self.smtp_state == self.COMMAND:
            sz, self.num_bytes = self.num_bytes, 0
            if not line:
                self.push('500 Error: bad syntax')
                return
            if not self._decode_data:
                line = str(line, 'utf-8')
            i = line.find(' ')
            if i < 0:
                command = line.upper()
                arg = None
            else:
                command = line[:i].upper()
                arg = line[i+1:].strip()
            max_sz = (self.command_size_limits[command]
                        if self.extended_smtp else self.command_size_limit)
            if sz > max_sz:
                self.push('500 Error: line too long')
                return
            method = getattr(self, 'smtp_' + command, None)
            if not method:
                self.push('500 Error: command "%s" not recognized' % command)
                return
            method(arg)
            return
        else:
            if self.smtp_state != self.DATA:
                self.push('451 Internal confusion')
                self.num_bytes = 0
                return
            if self.data_size_limit and self.num_bytes > self.data_size_limit:
                self.push('552 Error: Too much mail data')
                self.num_bytes = 0
                return
            # Remove extraneous carriage returns and de-transparency according
            # to RFC 5321, Section 4.5.2.
            data = []
            for text in line.split(self._linesep):
                if text and text[0] == self._dotsep:
                    data.append(text[1:])
                else:
                    data.append(text)
            self.received_data = self._newline.join(data)
            args = (self.peer, self.mailfrom, self.rcpttos, self.received_data, self.x_forward)
            kwargs = {}
            if not self._decode_data:
                kwargs = {
                    'mail_options': self.mail_options,
                    'rcpt_options': self.rcpt_options
                }
            status = self.smtp_server.process_message(*args, **kwargs)
            self._set_post_data_state()
            if not status:
                self.push('250 OK')
            else:
                self.push(status)

    # SMTP and ESMTP commands
    def smtp_HELO(self, arg):
        if not arg:
            self.push('501 Syntax: HELO hostname')
            return
        # See issue #21783 for a discussion of this behavior.
        if self.seen_greeting:
            self.push('503 Duplicate HELO/EHLO')
            return
        self._set_rset_state()
        self.seen_greeting = arg
        self.push('250 %s' % self.fqdn)

    def smtp_EHLO(self, arg):
        if not arg:
            self.push('501 Syntax: EHLO hostname')
            return
        # See issue #21783 for a discussion of this behavior.
        if self.seen_greeting:
            self.push('503 Duplicate HELO/EHLO')
            return
        self._set_rset_state()
        self.seen_greeting = arg
        self.extended_smtp = True
        self.push('250-%s' % self.fqdn)
        self.push('250-XFORWARD NAME PROTO HELO IDENT SOURCE ADDR')
        if self.data_size_limit:
            self.push('250-SIZE %s' % self.data_size_limit)
            self.command_size_limits['MAIL'] += 26
        if not self._decode_data:
            self.push('250-8BITMIME')
        if self.enable_SMTPUTF8:
            self.push('250-SMTPUTF8')
            self.command_size_limits['MAIL'] += 10
        self.push('250 HELP')
#        self.push('250-XFORWARD NAME ADDR PROTO HELO')

    def smtp_NOOP(self, arg):
        if arg:
            self.push('501 Syntax: NOOP')
        else:
            self.push('250 OK')

    def smtp_QUIT(self, arg):
        # args is ignored
        self.push('221 Bye')
        self.close_when_done()

    def smtp_XFORWARD(self,arg):
#        print(arg)
        self.x_forward += arg + ' '
        self.push('250 ok')

    def _strip_command_keyword(self, keyword, arg):
        keylen = len(keyword)
        if arg[:keylen].upper() == keyword:
            return arg[keylen:].strip()
        return ''

    def _getaddr(self, arg):
        if not arg:
            return '', ''
        if arg.lstrip().startswith('<'):
            address, rest = get_angle_addr(arg)
        else:
            address, rest = get_addr_spec(arg)
        if not address:
            return address, rest
        return address.addr_spec, rest

    def _getparams(self, params):
        # Return params as dictionary. Return None if not all parameters
        # appear to be syntactically valid according to RFC 1869.
        result = {}
        for param in params:
            param, eq, value = param.partition('=')
            if not param.isalnum() or eq and not value:
                return None
            result[param] = value if eq else True
        return result

    def smtp_HELP(self, arg):
        if arg:
            extended = ' [SP <mail-parameters>]'
            lc_arg = arg.upper()
            if lc_arg == 'EHLO':
                self.push('250 Syntax: EHLO hostname')
            elif lc_arg == 'HELO':
                self.push('250 Syntax: HELO hostname')
            elif lc_arg == 'MAIL':
                msg = '250 Syntax: MAIL FROM: <address>'
                if self.extended_smtp:
                    msg += extended
                self.push(msg)
            elif lc_arg == 'RCPT':
                msg = '250 Syntax: RCPT TO: <address>'
                if self.extended_smtp:
                    msg += extended
                self.push(msg)
            elif lc_arg == 'DATA':
                self.push('250 Syntax: DATA')
            elif lc_arg == 'RSET':
                self.push('250 Syntax: RSET')
            elif lc_arg == 'NOOP':
                self.push('250 Syntax: NOOP')
            elif lc_arg == 'QUIT':
                self.push('250 Syntax: QUIT')
            elif lc_arg == 'VRFY':
                self.push('250 Syntax: VRFY <address>')
            else:
                self.push('501 Supported commands: EHLO HELO MAIL RCPT '
                          'DATA RSET NOOP QUIT VRFY')
        else:
            self.push('250 Supported commands: EHLO HELO MAIL RCPT DATA '
                      'RSET NOOP QUIT VRFY')

    def smtp_VRFY(self, arg):
        if arg:
            address, params = self._getaddr(arg)
            if address:
                self.push('252 Cannot VRFY user, but will accept message '
                          'and attempt delivery')
            else:
                self.push('502 Could not VRFY %s' % arg)
        else:
            self.push('501 Syntax: VRFY <address>')

    def smtp_MAIL(self, arg):
        if not self.seen_greeting:
            self.push('503 Error: send HELO first')
            return
        print('===> MAIL', arg, file=DEBUGSTREAM)
        syntaxerr = '501 Syntax: MAIL FROM: <address>'
        if self.extended_smtp:
            syntaxerr += ' [SP <mail-parameters>]'
        if arg is None:
            self.push(syntaxerr)
            return
        arg = self._strip_command_keyword('FROM:', arg)
        address, params = self._getaddr(arg)
        if not address:
            self.push(syntaxerr)
            return
        if not self.extended_smtp and params:
            self.push(syntaxerr)
            return
        if self.mailfrom:
            self.push('503 Error: nested MAIL command')
            return
        self.mail_options = params.upper().split()
        params = self._getparams(self.mail_options)
        if params is None:
            self.push(syntaxerr)
            return
        if not self._decode_data:
            body = params.pop('BODY', '7BIT')
            if body not in ['7BIT', '8BITMIME']:
                self.push('501 Error: BODY can only be one of 7BIT, 8BITMIME')
                return
        if self.enable_SMTPUTF8:
            smtputf8 = params.pop('SMTPUTF8', False)
            if smtputf8 is True:
                self.require_SMTPUTF8 = True
            elif smtputf8 is not False:
                self.push('501 Error: SMTPUTF8 takes no arguments')
                return
        size = params.pop('SIZE', None)
        if size:
            if not size.isdigit():
                self.push(syntaxerr)
                return
            elif self.data_size_limit and int(size) > self.data_size_limit:
                self.push('552 Error: message size exceeds fixed maximum message size')
                return
        if len(params.keys()) > 0:
            self.push('555 MAIL FROM parameters not recognized or not implemented')
            return
        self.mailfrom = address
        print('sender:', self.mailfrom, file=DEBUGSTREAM)
        self.push('250 OK')

    def smtp_RCPT(self, arg):
        if not self.seen_greeting:
            self.push('503 Error: send HELO first');
            return
        print('===> RCPT', arg, file=DEBUGSTREAM)
        if not self.mailfrom:
            self.push('503 Error: need MAIL command')
            return
        syntaxerr = '501 Syntax: RCPT TO: <address>'
        if self.extended_smtp:
            syntaxerr += ' [SP <mail-parameters>]'
        if arg is None:
            self.push(syntaxerr)
            return
        arg = self._strip_command_keyword('TO:', arg)
        address, params = self._getaddr(arg)
        if not address:
            self.push(syntaxerr)
            return
        if not self.extended_smtp and params:
            self.push(syntaxerr)
            return
        self.rcpt_options = params.upper().split()
        params = self._getparams(self.rcpt_options)
        if params is None:
            self.push(syntaxerr)
            return
        # XXX currently there are no options we recognize.
        if len(params.keys()) > 0:
            self.push('555 RCPT TO parameters not recognized or not implemented')
            return
        self.rcpttos.append(address)
        print('recips:', self.rcpttos, file=DEBUGSTREAM)
        self.push('250 OK')

    def smtp_RSET(self, arg):
        if arg:
            self.push('501 Syntax: RSET')
            return
        self._set_rset_state()
        self.push('250 OK')

    def smtp_DATA(self, arg):
        if not self.seen_greeting:
            self.push('503 Error: send HELO first');
            return
        if not self.rcpttos:
            self.push('503 Error: need RCPT command')
            return
        if arg:
            self.push('501 Syntax: DATA')
            return
        self.smtp_state = self.DATA
        self.set_terminator(b'\r\n.\r\n')
        self.push('354 End data with <CR><LF>.<CR><LF>')

    # Commands that have not been implemented
    def smtp_EXPN(self, arg):
        self.push('502 EXPN not implemented')

		
class new_SMTPServer(asyncore.dispatcher):
    # SMTPChannel class to use for managing client connections
    channel_class = SMTPChannel

    def __init__(self, localaddr, remoteaddr,
                 data_size_limit=DATA_SIZE_DEFAULT, map=None,
                 enable_SMTPUTF8=False, decode_data=None):
        self._localaddr = localaddr
        self._remoteaddr = remoteaddr
        self.data_size_limit = data_size_limit
        self.enable_SMTPUTF8 = enable_SMTPUTF8
        if enable_SMTPUTF8:
            if decode_data:
                raise ValueError("The decode_data and enable_SMTPUTF8"
                                 " parameters cannot be set to True at the"
                                 " same time.")
            decode_data = False
        if decode_data is None:
            warn("The decode_data default of True will change to False in 3.6;"
                 " specify an explicit value for this keyword",
                 DeprecationWarning, 2)
            decode_data = True
        self._decode_data = decode_data
        asyncore.dispatcher.__init__(self, map=map)
        try:
            gai_results = socket.getaddrinfo(*localaddr,
                                             type=socket.SOCK_STREAM)
            self.create_socket(gai_results[0][0], gai_results[0][1])
            # try to re-use a server port if possible
            self.set_reuse_addr()
            self.bind(localaddr)
            self.listen(5)
        except:
            self.close()
            raise
        else:
            print('%s started at %s\n\tLocal addr: %s\n\tRemote addr:%s' % (
                self.__class__.__name__, time.ctime(time.time()),
                localaddr, remoteaddr), file=DEBUGSTREAM)

    def handle_accepted(self, conn, addr):
        print('Incoming connection from %s' % repr(addr), file=DEBUGSTREAM)
        channel = self.channel_class(self,
                                     conn,
                                     addr,
                                     self.data_size_limit,
                                     self._map,
                                     self.enable_SMTPUTF8,
                                     self._decode_data)

    # API for "doing something useful with the message"
    def process_message(self, peer, mailfrom, rcpttos, data,  **kwargs):
        """Override this abstract method to handle messages from the client.

        peer is a tuple containing (ipaddr, port) of the client that made the
        socket connection to our smtp port.

        mailfrom is the raw address the client claims the message is coming
        from.

        rcpttos is a list of raw addresses the client wishes to deliver the
        message to.

        data is a string containing the entire full text of the message,
        headers (if supplied) and all.  It has been `de-transparencied'
        according to RFC 821, Section 4.5.2.  In other words, a line
        containing a `.' followed by other text has had the leading dot
        removed.

        kwargs is a dictionary containing additional information. It is empty
        unless decode_data=False or enable_SMTPUTF8=True was given as init
        parameter, in which case ut will contain the following keys:
            'mail_options': list of parameters to the mail command.  All
                            elements are uppercase strings.  Example:
                            ['BODY=8BITMIME', 'SMTPUTF8'].
            'rcpt_options': same, for the rcpt command.

        This function should return None for a normal `250 Ok' response;
        otherwise, it should return the desired response string in RFC 821
        format.

        """
        raise NotImplementedError


