'''
Created on Jan 10, 2017

@author: tamsyn
'''
import basefilter
import rblquery
import filterfactory


class RBLFilter(basefilter.BaseFilter):
    '''
    classdocs
    '''

    def __init__(self, msg, params):
        '''
        Constructor
        '''
        basefilter.BaseFilter.__init__(self, "RBL")
        basefilter.BaseFilter.set_object(self, msg)
        basefilter.BaseFilter.set_param(self, params)
        
        self.filter = rblquery.Query(params['ip'])
    
    def Execute(self):
        self.result = self.filter.spamhaus_lookup()


if __name__ == '__main__':
    param = {}
    param['ip'] = '123.27.90.88'
    param['timeout'] = 2
    
    rbl = RBLFilter("", param)
    rbl.Execute()
    res = rbl.get_result()
    print("Execute result : %s" % res)
elif __name__ == 'rblfilter':
    filterfactory.factory.register_filter(RBLFilter)

