#!/usr/bin/python3.5

#https://www.spamhaus.org/faq/section/DNSBL%20Usage#200
rbl = { 
       '127.0.0.10':'PBL',
       '127.0.0.11':'PBL',
       '127.0.0.9':'SBL',
       '127.0.0.2':'SBL',
       '127.0.0.3':'SBL',
       '127.0.0.4':'XBL',
       '127.0.0.5':'XBL',
       '127.0.0.6':'XBL',
       '127.0.0.7':'XBL'
    
    }

dbl = {'127.0.1.2':'Spam Domain',
       '127.0.1.4':'Phish Domain',
       '127.0.1.5':'Malware Domain',
       '127.0.1.6':'Botnet C&C Domain',
       '127.0.1.102':'abused legit spam',
       '127.0.1.103':'abused spammed redirector domain',
       '127.0.1.104':'abused legit phish',
       '127.0.1.105':'abused legit malware',
       '127.0.1.106':'abused legit botnet C&C',
       '127.0.1.255':'IP queries prohibited!'
       }


sbl='sbl'
pbl='pbl'
xbl='xbl'

