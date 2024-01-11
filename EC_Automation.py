###_______________________________________________________________________________________________## 
#This is a test script for automating EC Number extraction. 
##This needs to take in a URL and extract just the ID from it, and put it into a CSV file so it can
##fit into the existing _3_ script. 
from datetime import datetime
import requests
from fake_useragent import UserAgent
import time
from Bio import ExPASy
from Bio import SwissProt
from Bio.ExPASy import Enzyme
import os
###_______________________________________________________________________________________________##
def EC_extract():
    now = datetime.now()
    str_date = now.strftime("%Y_%m_%d")
    ec_library = 'EC_library' + '_' + str_date
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    ec_url = 'https://ftp.expasy.org/databases/enzyme/enzyme.dat'
    time.sleep(4)
    ec = requests.get(ec_url, headers=header)
    if ec.status_code == 200:
        with open(ec_library, 'w+') as ec_file:
            ec_file.write(ec.text)
    print('EC List Has Been Created')
###_______________________________________________________________________________________________
    handle = open(ec_library)
    records = Enzyme.parse(handle)
    ecnumbers = [record["ID"] for record in records]
    print(type(ecnumbers)) #This is a list at this point in the code
    path = os.path.abspath(ec_library)
    with open(path, 'w+') as txt_file:
        for item in ecnumbers:
            txt_file.write("%s\n" % item)
    print('EC list Has Been Created')
EC_extract()