import socket

class Query():
    def rbl_lookup(self,reverse_ip):
        self.reverse_ip=reverse_ip
        print(reverse_ip)
        try:
            ret = socket.gethostbyname('%s.%s'% (reverse_ip,'zen.spamhaus.org'))
            return(ret)
        except ValueError as err:
            return(err)

