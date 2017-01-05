#!/usr/bin/python3.5
class IPValidator():
    """
    Return Dict:
    Key Value Pair
    valid_ip_bool = Result of Validate IP (boolean)
    valid_ip = IP Validated
    valid_ip_err = Any Value Errors generated when trying to validate the IP
    Origional_ip=Request we received
    reverse_ip = IP reversed
    reverse_ip_bool = Result of Reverse IP (boolean)
    reverse_ip_err = Any Value Errors generated when trying to reverse the IP
    """
    def __init__(self,address):
        self.address=address
        self.ret={}
    def validate_ip(self):
        self.ret["original_ip"]=self.address
        
        try:
            host_bytes = self.address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            self.ret["valid_ip_bool"]=True
            self.ret["valid_ip"]=self.address
            return(self.ret)
        
        except ValueError as err:
            #print(err)
            self.ret['valid_ip_bool']=False
            self.ret['valid_ip_err']=err
            return (self.ret)
    
    def reverse_ip(self):
        if not (self.validate_ip()['valid_ip_bool']):
            self.ret['reverse_ip_bool']=False
            self.ret['reverse_ip_err']='Unable to validate IP'
            return(self.ret)#Unable to Validate IP
        #Possibly change Return into Dictionary?? {bool: true, reverse_ip: reverse}
        else:
            try:
                parsed = self.address.split('.')
                parsed.reverse()
                self.ret['reverse_ip_bool']=True
                self.ret['reverse_ip']='.'.join(parsed)
                return(self.ret)
            except ValueError as err:
                #print(err)
                self.ret['reverse_ip_bool']=Fase
                self.ret['reverse_ip_err']=err
                return(self.ret)
            
#print(IPValidator('2.2.2.adfadf').reverse_ip())