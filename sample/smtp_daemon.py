'''
Created on Jan 22, 2018

@author: root
'''
# coding:utf-8

import smtpd
import asyncore
import time
import uuid

from azure.storage.queue import QueueService
from azure.storage.file import FileService
from azure.storage.file import ContentSettings

myaccount = "emaildev"
mykey = "bMtI6Il0Sax7vNr8SFlL75ZMB0OksA1ZYsJ0bpT/RuyI15t1ieZcpY6DkEtWggc9sK7YdN0Mxym05JFtmIpXZg=="

queue_service = QueueService(account_name=myaccount, account_key=mykey)
file_service = FileService(account_name=myaccount, account_key=mykey)

# generator = file_service.list_directories_and_files('smbesg')
# for file_or_dir in generator:
#     print(file_or_dir.name)
    
import random

def GetRandomTable(length):
    rnd = ''

    for i in range(1,length+1):
        key = random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
        rnd += key

    return rnd
#end of GetRandomTable

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
        
        #queue_id = str(uuid.uuid4())
        queue_id = GetRandomTable(10)
        
        queue_service.put_message('mailpool', queue_id.decode('ascii'))
        file_service.create_file_from_text('smbesg', None, queue_id,
                              data, encoding='utf-8', 
                              content_settings=ContentSettings(content_type='text/plain'))
        
        print("message processed")
        print("message id: %s" % queue_id)
        return


if __name__ == '__main__':
    server = CustomSMTPServer(('0.0.0.0', 25), None)
    asyncore.loop()
