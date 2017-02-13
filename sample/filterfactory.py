'''
Created on Feb 13, 2017

@author: tamsyn
'''

factory = None

class FilterFactory():
    '''
    classdocs
    '''
    def __init__(self):
        self.filter_map = []
        
    def register_filter(self, filter_object):
        self.filter_map.append(filter_object)
    
    def get_filters(self):
        pass
    
if __name__ == 'filterfactory':
    if factory == None:
        factory = FilterFactory()
    