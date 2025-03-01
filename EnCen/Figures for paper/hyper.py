import pandas as pd
from scipy.stats import hypergeom
from sklearn.cluster import KMeans

percentages = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/all_biomes_percentage.xlsx')

transposed = percentages.T
# print(transposed)
# dropped = percentages.drop(columns=['Biome'], errors='ignore')
transposed.columns = transposed.iloc[0]
transposed1 = transposed[1:]


kmeans = KMeans(init='random', n_clusters=5, n_init=10, random_state=252)
transposed1['Cluster'] = kmeans.fit_predict(transposed1)

cluster = transposed1

cluster.sort_values("Cluster", axis=0, ascending=True, inplace=True)

reset = cluster.reset_index()

reset['EC'] = reset['index'].str.split('_').str[0]


reset2 = reset.drop(['index', 'Activated Sludge', 'Bulk Soil', 'Cow Rumen', 'Lake Sediment', 'River Sediment'], axis = 1)
reset2.columns.name  = None


reset2 = reset2.astype(int)


# print(zero)
result = reset2.groupby('Cluster')['EC'].sum()
reuslt2 = reset2.groupby('EC')['Cluster'].sum()
result3 = reset2.groupby('Cluster')['EC'].value_counts()
print(result)
print(reuslt2)
print(result3)
