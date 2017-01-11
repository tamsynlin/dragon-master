#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

'''
Created on Dec 6, 2016

@author: tamsyn
'''
import email
import re
from html.parser import HTMLParser
from urllib.parse import urlparse


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.urls = []
        HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, print it.
                if name == "href":
                    #print (name, "=", value)
                    self.urls.append(urlparse(value))
    def get_urls(self):
        return self.urls

class DragonParser():
    def __init__(self, email_content):
        self.email_content = email_content
        self.html_parser = MyHTMLParser()
        self.html_parser.reset()
        self.atts = {}
        
    def __del__(self):
        self.html_parser.close()
    
    def get_url_list(self):
        return self.html_parser.get_urls()
    
    def get_attachments(self):
        return self.atts
    
    def extract_url_from_text(self, text):
        """
        The regex patterns in this gist are intended to match any URLs,
        including "mailto:foo@example.com", "x-whatever://foo", etc. For a
        pattern that attempts only to match web URLs (http, https), see:
        https://gist.github.com/gruber/8891611
        """
        ANY_URL_REGEX = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?������]))"""
        rule=re.compile(ANY_URL_REGEX, flags=0)
        """
        The regex patterns in this gist are intended only to match web URLs -- http,
        https, and naked domains like "example.com". For a pattern that attempts to
        match all URLs, regardless of protocol, see: https://gist.github.com/gruber/249502
        """
        WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?������])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        stri_text=text.decode(encoding='utf-8')
        urls = rule.findall(stri_text)
        #print(urls)
    def extract_url_from_html(self, html):
        self.html_parser.feed(html.decode(encoding='utf-8'))
        #html_p = MyHTMLParser()
        #html_p.feed(html.decode(encoding='utf-8'))
    
    def ParserEmail(self):
        b = email.message_from_string(self.email_content)
        #print(b)
        print(b['from'])
        print(b['to'])
        
        if b.is_multipart():
            for part in b.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
        
                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    #print(body)
                    self.extract_url_from_text(body)
                    #extract URL
                elif ctype == 'text/html' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)  # decode
                    #print(body)
                    #extract URL
                    self.extract_url_from_html(body)
                elif 'attachment' not in cdispo:
                    print("Attachment name %s" % cdispo['attachment'])
                    attachment = part.get_payload(decode=False)
                    self.atts[cdispo['attachment']] = attachment
                    
        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
        else:
            body = b.get_payload(decode=True)
            print(body)


if __name__ == '__main__':
    f = open('test.msg', "r")
    email_content = f.read()
    
    parser = DragonParser(email_content)
    parser.ParserEmail()
    urls= parser.get_url_list()
    #print(urls)
    
    atts = parser.get_attachments()
    
    f.close()
