#August 6th, 2024
#This is a script that takes in a metagenomic functional profile and (hopefully) returns the bins that contain a specific enzyme. 


import pandas as pd 
import numpy as np


##Data cleaning and processing____________________________________________________________
profile = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC Results/Activated_Sludge/functional_profiles/Activated_Sludge_Metagenome_functional_profile', header=None)
funcprof = profile.iloc[:,0].str.split(' ', expand=True)
funcprof.columns = funcprof.iloc[0] #assigns the first row (iloc[0] to the columns of the dataframe)
funcprof = funcprof[1:] #creates a new dataframe from the second row onward. 
    
    # funcprof.to_excel('Funcprof2.xlsx', index=False)

for col in funcprof.columns[1:]:
    funcprof[col] = pd.to_numeric(funcprof[col])

print(funcprof.head(5))

##Bin Search
value = 1
enzyme = '4.1.1.116'
result = funcprof[funcprof[enzyme] == value]
result = result['Name_of_Genome']

print(result)