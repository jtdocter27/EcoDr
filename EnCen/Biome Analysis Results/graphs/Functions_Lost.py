##August 2nd, 2024
##This scirpt shows a bivariate blot of rare functions in the specified biome. 
##This script also shows a displot of the counts of each EC Plot. 

import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

activated_sludge = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Biome Analysis Results/Activated Sludge/Lost_Functions.xlsx')
# print(activated_sludge.head(10))

def EC_parse1(value):
    parts = (value.split('.'))
    return float('.'.join(parts[:2]))

def EC_parse2(value):
    parts = (value.split('.'))
    return float('.'.join(parts[:1]))

activated_sludge['EC Class'] = activated_sludge['EC Number'].apply(EC_parse1)
activated_sludge2 = activated_sludge[['EC Class', 'Percentage', 'Name']]
print(activated_sludge2)




sns.displot(data=activated_sludge2, x= 'EC Class', y='Percentage') #Bivariate Plot 
plt.title('Percentages of Rare Functions Grouped by EC Class and Subclass')
plt.show()


activated_sludge['EC Class'] = activated_sludge['EC Number'].apply(EC_parse2)
activated_sludge3 = activated_sludge[['EC Class', 'Percentage', 'Name']]
sns.displot(data=activated_sludge3, x= 'EC Class', kde=True) #hist, counts vs. EC
plt.title('Counts of Rare Functions Grouped by EC Class')
plt.show()
