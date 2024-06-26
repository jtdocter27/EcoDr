###_______________________________________________________________________________________________## 
#This is a test script for automating EC Number extraction. 
##This needs to take in a URL and extract just the ID from it, and put it into a CSV file so it can
##fit into the existing _3_ script. 
import requests
from fake_useragent import UserAgent
import time
from Bio import ExPASy
from Bio import SwissProt
from Bio.ExPASy import Enzyme
import pandas as pd 
import os
###_______________________________________________________________________________________________##
def EC_extract():
    ec_library = 'EC_library.csv'
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    ec_url = 'https://ftp.expasy.org/databases/enzyme/enzyme.dat'
    time.sleep(4)
    ec = requests.get(ec_url, headers=header)
    if ec.status_code == 200:
        with open(ec_library, 'w+', newline='\n') as ec_file:
            ec_file.write(ec.text)
    print(type(ec_file))
    print('EC List Has Been Created')
###_______________________________________________________________________________________________
    handle = open(ec_library)
    records = Enzyme.parse(handle)
    ecnumbers = [record['ID'] for record in records]
    handle2 = open(ec_library)
    records = Enzyme.parse(handle2)
    ecnames = [record['DE'] for record in records]
    print(type(ecnumbers)) #This is a list at this point in the code
    together = pd.DataFrame({'EC Number': ecnumbers, 'Name': ecnames})
    together.to_csv('EC_name_&_num.csv', index=False)

EC_extract()