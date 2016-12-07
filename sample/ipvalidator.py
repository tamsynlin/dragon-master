class IPValidator():
    def __init__(self,address):
        self.address=address
    def validate_ip(self):
        try:
            host_bytes = self.address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            return (host_bytes)
        except ValueError as err:
            #print(err)
            return (False)
    def reverse_ip(self):
        if not (self.validate_ip()):
            return(False)#Unable to Validate IP
        else:
            try:
                parsed = self.address.split('.')
                parsed.reverse()
                return('.'.join(parsed))
            except ValueError as err:
                #print(err)
                return(False)

