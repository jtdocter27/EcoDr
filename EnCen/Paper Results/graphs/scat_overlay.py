#August 5nd, 2024
##This script shows the overlay of EC vs. topmatch presence/abscence and Synbio vs. topmatch presence/abscence

import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import re

activated_sludge = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Paper Results/Biome Analysis Results/Activated Sludge/Biome Synbio Top Match EC Comparison.xlsx')
# print(activated_sludge.dtypes)

activated_sludge['EC subclass'] = activated_sludge['EC Number'].str.extract(r'^\d+\.(\d+)', expand = False)
activated_sludge['EC class'] = activated_sludge['EC Number'].str.extract(r'^(\d+)', expand = False) #converts the series into strings (previously objects), .extarct takes out specfic patterns, r denotes raw string, ^ asserts the position at the start of the string, \d matches any digit, () creates a group 
print(activated_sludge)
print(activated_sludge.dtypes)

activated_sludge['EC subclass'] = activated_sludge['EC subclass'].astype(int)
activated_sludge['EC Class'] = activated_sludge['EC class'].astype(int)
print(activated_sludge.dtypes)

activated_sludge_tm = activated_sludge[['EC Class', 'EC subclass', 'Top Match Presence/Absence']]
activated_sludge_syn = activated_sludge[['EC Class', 'EC subclass', 'Synbio Presence/Absence' ]]

fig, ax = plt.subplots()
sns.scatterplot(data=activated_sludge_tm, x = 'EC Class', y = 'EC subclass', ax=ax)
sns.scatterplot(data=activated_sludge_syn, x = 'EC Class', y = 'EC subclass', ax=ax)
plt.show()
