from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing



binary = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Figures for paper/AllBiomesBinaryFinal.txt', delimiter = '\t', index_col= 0)
binary.index #index is our genomes
binary['Biome'] = binary['Biome'].astype('category')
# binary.dtypes
sums = binary.loc[ :, binary.columns != 'Biome']
sums = sums.sum()
counts = binary['Biome'].value_counts()
counts = pd.DataFrame(counts)
counts = counts.rename(index={'ActivatedSludge': 'Activated Sludge', 'BulkSoil': 'Bulk Soil', 'LakeSediment': 'Lake Sediment', 'CowRumen':'Cow Rumen', 'RiverSediment':'River Sediment'})
counts = counts.rename(columns={'count': 'Total Genomes'})
counts = counts.reset_index()
column_sums = binary.groupby(by='Biome', observed=False).sum()
ec_sums = pd.DataFrame(column_sums)
clean = ec_sums.rename(index={'ActivatedSludge': 'Activated Sludge', 'BulkSoil': 'Bulk Soil', 'LakeSediment': 'Lake Sediment', 'CowRumen':'Cow Rumen', 'RiverSediment':'River Sediment'})
# for col in clean.columns:
#     if clean[col].sum()<=100:
#         del clean[col]
# print(ec_sums)
clean.iloc[0] = clean.iloc[0].div(1374).astype('float64')
clean.iloc[1] = clean.iloc[1].div(2267).astype('float64')
clean.iloc[2] = clean.iloc[2].div(1293).astype('float64')
clean.iloc[3] = clean.iloc[3].div(2183).astype('float64')
clean.iloc[4] = clean.iloc[4].div(633).astype('float64')







# drop_biome = clean.reset_index()
# drop_biome2 = drop_biome.drop('Biome', axis=1)
# biome = drop_biome['Biome']



# kmeans = KMeans(n_clusters=5, random_state=42)
# kmeans.fit(drop_biome2)

# labels = kmeans.labels_
# # print(labels)
# centroids = kmeans.cluster_centers_

# sns.scatterplot(data=drop_biome)
# plt.show()