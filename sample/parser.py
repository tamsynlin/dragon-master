#!/root/Python-3.5.2/python 
import os
import sys

class Parser():
    def __init__(self,data):
        self.data = data
    def x_header_parse(self):
        print(self.data)
        a=self.data.split(' ')[0]
        b=self.data.split(' ')
        print(a)
        print(b)

Parser('ADDR=10.0.0.5 PROTO=ESMTP HELO=[string] IDENT=E1BF64FF2FE  SOURCE=RMOTE').x_header_parse()