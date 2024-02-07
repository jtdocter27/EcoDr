import pandas as pd
import numpy as np
import requests

url =  'https://websvc.biocyc.org/st-get?id=biocyc13-86497-3916238843&format=tsv' #https://websvc.biocyc.org/st-get?id=[SMARTTABLE-ID]&format=[json|xml|tsv]
url = requests.get(url)
path = 'All_Reactions_of_MetaCyc'
if url.status_code == 200:
    with open(path, 'wb') as path:
        path.write(url.content)
    print("All Reactions of Metacyc Succesfully Downloaded")
else:
    print(f"Nump Nump Nump Try Again. Status code: {url.status_code}")
