class IPValidator():
    def __init__(self,address):
        self.address=address
    def validate_ip(self):
        try:
            host_bytes = self.address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            return (len(host_bytes) == 4 and len(valid) == 4, host_bytes)
        except ValueError as err:
            return (False,err)
    def reverse_ip(self):
        if not (self.validate_ip()[0]):
            return(False,'IP Invalid %s' % self.validate_ip()[1])
        else:
            try:
                parsed = self.address.split('.')
                parsed.reverse()
                return(True, '.'.join(parsed))
            except:
                return(False,'Unable to reverse address %s' % self.address)

