#!/root/Python-3.5.2/python 
import os
import sys

class Parser():
    def __init__(self,data):
        self.data = data
    def x_header_parse(self):
        """Returns a dictionary of X Headers"""
        ret={}#parse the X Headers on 
        for value in self.data:
            print(value)
            ret[value.split('=')[0]] = value.split('=')[1]
            continue
        return(True, value)