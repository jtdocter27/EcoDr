###September 25th, 2024 
###The function of this script is to screen the synbio genome for enzymes that ensure survival and stress response in a given environment 

import pandas as pd 
import numpy as np 
from bioservices import KEGG
kegg = KEGG()


#___________________________________

##Data Processing 
perc_df = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Paper Results/Biome Analysis Results/Cow Rumen/Biome Synbio Top Match EC Comparison.xlsx')
fifty = perc_df[perc_df['Percentage'] > 0] 
fifty = fifty.drop(columns = ['Top Match Presence/Absence'])
# print(fifty)

##Enzymes to search 
enzyme = 'amylase'
enzyme2 = 'pullulanase'
enzyme3 = 'glucanase'


##Searching enzymes 
result = fifty[fifty['Name'].str.contains(enzyme, case=False, na=False, regex=True)]
# print(result)
result2 = fifty[fifty['Name'].str.contains(enzyme2, case=False, na=False, regex=True)]
# print(result2)
result3 = fifty[fifty['Name'].str.contains(enzyme3, case=False, na=False, regex=True)]
# print(result3)

##putting all enzyme returns together 
stack = pd.concat([result, result2, result3], ignore_index=True)
print(stack)
















