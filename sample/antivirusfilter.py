import basefilter
import antivirus_lookup


class AVFilter(basefilter.BaseFilter):
    '''
    classdocs
    '''

    def __init__(self, attachment, params):
        '''
        Constructor
        '''
        basefilter.BaseFilter.__init__(self, "AntiVirus")
        basefilter.BaseFilter.set_object(self, attachment)
        basefilter.BaseFilter.set_param(self, params)        
        self.filter = avscanner(attachment)
    
    def Execute(self):
            self.result=self.filter.scan_buffer()
            
        #self.result = self.filter.spamhaus_lookup()


if __name__ == '__main__':
    param = {}
    param['ip'] = '123.27.90.88'
    param['timeout'] = 2
    
    #rbl = RBLFilter("", param)
    #rbl.Execute()
    #res = rbl.get_result()
    print("Execute result : %s" % res)

