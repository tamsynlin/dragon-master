'''
Created on Jan 10, 2017

@author: tamsyn
'''

ByPassed = "By passed"
Triggered = "Triggered"
NotTriggered = "Not Triggered"
Nothing = "Nothing"

class BaseFilter():
    '''
    Basic interface that all the plug-in need to implement
    '''
    def __init__(self, filtertype):
        '''
        Constructor
        '''
        self.type = filtertype
        self.obj = "";
        self.param = {}
        self.result = Nothing
    
    def get_type(self):
        return self.type
    
    def set_object(self, msg):
        self.obj = msg
    
    def set_param(self, paramters):
        self.param = paramters
    
    def Execute(self):
        pass
    
    def Log(self):
        pass
    
    def get_result(self):
        return self.result
