import pyclamd

class avscanner():

    def __init__(self, attachment):
        self.attachment = attachment
        self.ret = {}
        
        
    def connect(self):
        try:
            self.scanner=pyclamd.ClamdAgnostic()
            if self.scanner.ping()==True:
                self.ret['av_connect_bool']=True
        except ValueError as error :
            self.ret['av_connect_bool']=False
            self.ret['av_connect_err']=error
        return(self.ret)
    
    
    def scan_buffer(self):
        connect()
        try:
            if self.ret['av_connect_bool'] != False:
                results = self.scanner.scan_stream(self.attachment)
                if "FOUND" not in results[0]:
                    self.ret['av_virus_found']=False                
                elif "FOUND" in results [0]:
                    self.ret['av_virus_found']=True
                    self.ret['av_virus_name']=results[1]
            self.ret['av_virus_bool']=True
        except ValueError as error:
            self.ret['av_virus_bool']=False
            self.ret['av_virus_err']=error
        return(self.ret)