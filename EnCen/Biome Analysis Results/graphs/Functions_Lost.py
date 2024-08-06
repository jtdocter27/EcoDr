##August 2nd, 2024
##This scirpt shows a bivariate blot of rare functions in the specified biome. 
##This script also shows a displot of the counts of each EC Plot. 

import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

activated_sludge= pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Biome Analysis Results/Activated Sludge/Lost_Functions.xlsx')
activated_sludge_all = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Biome Analysis Results/Activated Sludge/Biome Synbio Top Match EC Comparison.xlsx')
 #remember lost functions are just those that the topmatch bin has and the invading organism does not have. 
# print(activated_sludge.head(10))

def EC_parse1(value):
    parts = (value.split('.'))
    return float('.'.join(parts[:2]))

def EC_parse2(value):
    parts = (value.split('.'))
    return float('.'.join(parts[:1]))

activated_sludge['EC Class and Subclass'] = activated_sludge['EC Number'].apply(EC_parse1)
activated_sludge2 = activated_sludge[['EC Class and Subclass', 'Percentage', 'Name']]
print(activated_sludge2)




sns.displot(data=activated_sludge2, x= 'EC Class and Subclass', y='Percentage', color = 'red', kind="kde", rug=True) #Bivariate Plot 
plt.legend()
plt.title('Percentages of Rare Functions Grouped by EC Class and Subclass')
plt.xticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7.5])
plt.show()


activated_sludge['EC Class'] = activated_sludge['EC Number'].apply(EC_parse2)
activated_sludge3 = activated_sludge[['EC Class', 'Percentage', 'Name']]
print(activated_sludge3)
sns.displot(data=activated_sludge3, x= 'EC Class') #hist, counts vs. EC
plt.title('Counts of Rare Functions Grouped by EC Class')
plt.show()


activated_sludge_all = activated_sludge_all[activated_sludge_all['Percentage'] !=0.0]
print(activated_sludge_all)


plt.figure(figsize=(12, 12))
sns.scatterplot(data= activated_sludge_all, x='Percentage', y='EC Number', color = 'black', label = 'All Biome')
sns.scatterplot(data= activated_sludge, x='Percentage', y='EC Number', color='red', label='Displaced Functions')
# plt.yticks(rotation=75)
y_values = activated_sludge['EC Number'].values
plt.yticks(ticks=y_values)
plt.title('Metagenome Lost Functions')
plt.show()