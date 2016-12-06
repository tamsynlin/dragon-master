#!/root/Python-3.5.2/python 
import socket
from t_variable import v_rbl

class Query():
    #def __init__(self, ip):
    def rbl_lookup(self,reverse_ip):
        self.reverse_ip=reverse_ip
        value='Null'
        ret='Error'
        try:
            dns_result = socket.gethostbyname('%s.%s'% (reverse_ip,'zen.spamhaus.org'))#https://www.spamhaus.org/faq/section/DNSBL%20Usage#200
            third_octect=int(dns_result.split('.')[3])
            ip_parse=dns_result.split('.')
            if not(int(ip_parse[0])==127) or not int(ip_parse[1])==0 or not (int(ip_parse[2])==0):
                ret = ('DNS response is not a valid SBL response [%s]' % ip_parse)
            else:
                ret=dns_result
                if 10 <=  third_octect <= 11:
                    value=v_rbl.pbl
                elif(2<=third_octect<=3) or (third_octect==9) :
                    value=v_rbl.sbl
                elif (4<=third_octect<=7):
                    value=v_rbl.xbl
                else:
                    value='Undefined'
        
        except:
            ret = ('Unable to match %s to any RBL' % reverse_ip)
        return(ret, value)            

