#!/root/Python-3.5.2/python 
import socket

class Query():
    def rbl_lookup(self,reverse_ip):
        self.reverse_ip=reverse_ip
        value='Null'
        try:
            ret = socket.gethostbyname('%s.%s'% (reverse_ip,'zen.spamhaus.org'))#https://www.spamhaus.org/faq/section/DNSBL%20Usage#200
            third_octect=int(ret.split('.')[3])
            if 10 <=  third_octect <= 11:
                value='PBL'
            elif(2<=third_octect<=3) or (third_octect==9) :
                value='SBL'
            elif (4<=third_octect<=7):
                value='XBL'
            return(ret,value)
        except:
            ret = ('Unable to match %s to any RBL' % reverse_ip)
            return(ret)


