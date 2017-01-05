#!/usr/bin/python3.5
import socket
from ipvalidator import IPValidator
from t_variable import dbl, rbl

class Query():
    def __init__(self, data):
        self.data=data
        self.ret=IPValidator(data).reverse_ip()
        self.ret['query_data']=data
        #self.reverse_ip=''
    def spamhaus_lookup(self):
        data=self.data
        if not self.ret['valid_ip_bool']:
            try:
               self.dbl_lookup()
            except ValueError as err:
                #print(err)
                self.ret['dbl_query_bool']=False
                self.ret['dbl_error']=err
                #unable to match DBL Lookup
        else:
                #ip=data
                #self.reverse_ip=IPValidator(ip).reverse_ip()
                #print(self.ret)
                if not (self.ret['reverse_ip_bool']==False):
                    self.rbl_lookup()
                else:
                    self.ret['rbl_query_bool']=False
        return(self.ret)
    def dbl_lookup(self):#dbl.spamhaus.org
        #Domain
        #
        try:
            dns_result=socket.gethostbyname('%s.%s' % (self.data, 'dbl.spamhaus.org'))
            self.ret['dbl_query_ip']=dns_result
            if dns_result in self.dbl:
                self.ret['dbl_query_value']=self.dbl[dns_result]
            else: 
                self.ret['dbl_query_value']="Unknown Result"
            self.ret['dbl_query_bool']=True
        except ValueError as err:
            self.ret['dbl_query_bool']=False
            self.ret['dbl_query_err']=err
        
        #print(dns_result)
        return()
    def rbl_lookup(self):
        reverse_ip=self.ret['reverse_ip']
        value='Null'
        ret='Error'
        try:
            dns_result = socket.gethostbyname('%s.%s'% (reverse_ip,'zen.spamhaus.org'))
            self.ret['rbl_query_ip']=dns_result
            if dns_result in self.rbl:
                self.ret['rbl_query_value']=self.rbl[dns_result]
            else: 
                self.ret['rbl_query_value']="Unknown Result"
            self.ret['rbl_query_bool']=True
            #https://www.spamhaus.org/faq/section/DNSBL%20Usage#200
            
            #third_octect=int(dns_result.split('.')[3])
            #ip_parse=dns_result.split('.')
            #if not(int(ip_parse[0])==127) or not int(ip_parse[1])==0 or not (int(ip_parse[2])==0):
            #    ret = ('DNS response is not a valid SBL response [%s]' % ip_parse)
            #else:
            #    ret=dns_result
            #    if 10 <=  third_octect <= 11:
            #        value=pbl
            #   elif(2<=third_octect<=3) or (third_octect==9) :
            #       value=sbl
            #    elif (4<=third_octect<=7):
            #        value=xbl
            #    else:
            #        value='Undefined'

                
                
        except ValueError as err:
            self.ret['rbl_query_bool']=False
            self.ret['rbl_query_error']=err
        return()            

print(Query('2.2.2.2').spamhaus_lookup())
