###September 25th, 2024 
###The function of this script is to screen the synbio genome for enzymes that ensure survival and stress response in a given environment 

import pandas as pd 
import numpy as np 
from bioservices import KEGG
kegg = KEGG()


#___________________________________

###import Biome synbio top match EC comparison from EnCen 
##parse for only synbio presence/absence 
perc_df = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Paper Results/Biome Analysis Results/Cow Rumen/Biome Synbio Top Match EC Comparison.xlsx')
fifty = perc_df[perc_df['Percentage'] > 0] 
fifty = fifty.drop(columns = ['Top Match Presence/Absence'])
# print(fifty)

enzyme = 'amylase'
enzyme2 = 'pullulanase'
enzyme3 = 'glucanase'

result = fifty[fifty['Name'].str.contains(enzyme, case=False, na=False, regex=True)]
# print(result)
result2 = fifty[fifty['Name'].str.contains(enzyme2, case=False, na=False, regex=True)]
# print(result2)
result3 = fifty[fifty['Name'].str.contains(enzyme3, case=False, na=False, regex=True)]
# print(result3)


stack = pd.concat([result, result2, result3], ignore_index=True)
print(stack)

# present = fifty[fifty['Synbio Presence/Absence'] == 1]
# print(present) #This is a dataframe of all present synbio enzymes that occur in over 50% of the bins 
# enzyme_name = fifty['Name']
# print(enzyme_name)




##List of necessary functions for survival (where will this come from...)
# kegg.organism = 'vna'
# print(kegg.pathwayIds)


# enzyme_data = kegg.list('pathway', 'vna')
# print(enzyme_data)

# data = kegg.get('vna00620')
# print(data)













##merge lists 






##Score - make it so if the synbio org has it, keeps a 1, if it doesn't 0. Or something. 





