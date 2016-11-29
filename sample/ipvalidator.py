#!/root/Python-3.5.2/python 
class IPValidator():
    def validate_ip(self,address):
        self.address=address
        try:
            host_bytes = address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            return (len(host_bytes) == 4 and len(valid) == 4, host_bytes)
        except ValueError as err:
            return (False,err)
    def reverse_ip(self,address):
        self.address = address
        try:
            parsed = address.split('.')
            parsed.reverse()
            return(True, '.'.join(parsed))
        except:
            return(False,'Unable to reverse address %s' % address)
