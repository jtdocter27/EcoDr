import pandas as pd
import numpy as np
import requests

url =  'https://websvc.biocyc.org/st-get?id=biocyc13-86497-3916238843&format=tsv' #https://websvc.biocyc.org/st-get?id=[SMARTTABLE-ID]&format=[json|xml|tsv]
url = requests.get(url)
path = 'All-reactions-of-MetaCyc.txt'
if url.status_code == 200:
    with open(path, 'wb') as path:
        path.write(url.content)
    print("All Reactions of Metacyc Succesfully Downloaded")
else:
    print(f"Nump Nump Nump Try Again. Status code: {url.status_code}")
MC = pd.read_csv('All-reactions-of-MetaCyc.txt', delimiter='\t')
MCEdit = MC[MC['Reaction'].str.contains('SUBSEQ,|\'end\'|(3)|is|beyond|the|end|of|the|sequence|(2).') == False]
#MCEdit2 = MCEdit[MCEdit[]]
strings_to_remove = ['SUBSEQ,','\'end\'', '(3)', 'is', 'beyond', 'the', 'end', 'of', 'the', 'sequence', '(2).' ]
MCEdit.to_csv('All-reactions-of-MetaCyc.txt', sep='\t', index=False)