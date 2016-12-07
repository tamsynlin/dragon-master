#!/root/Python-3.5.2/python 
import os
import sys

class Parser():
    def __init__(self,data):
        self.data = data
    def x_header_parse(self):
        """Returns a dictionary of X Headers"""
        ret={}#parse the X Headers on 
        for value in self.data.split(' '):
            print(value)
            if "=" in value:
               ret[value.split('=')[0]] = value.split('=')[1]
            continue
        return(ret)
    
#print(Parser('ADDR=2.2.2.2  PROTO=ESMTP HELO=[1.2.3.4] IDENT=39B4741C4547 SOURCE=REMOTE').x_header_parse())