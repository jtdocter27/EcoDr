from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import parallel_coordinates
from scipy.stats import hypergeom


percentages = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/all_biomes_percentage.xlsx')

transposed = percentages.T
# print(transposed)
# dropped = percentages.drop(columns=['Biome'], errors='ignore')
transposed.columns = transposed.iloc[0]
transposed1 = transposed[1:]
# print(transposed1)

num_clusters = 50
kmeans_tests = [KMeans(n_clusters=i, init='random', n_init=10) for i in range(1, num_clusters)]
score = [kmeans_tests[i].fit(transposed1).score(transposed1) for i in range(len(kmeans_tests))]

# # Plot the curve
plt.plot(range(1, num_clusters),score)
plt.xlabel('Number of Clusters')
plt.ylabel('Variance')
# plt.show()

kmeans = KMeans(init='random', n_clusters=5, n_init=10)
transposed1['Cluster'] = kmeans.fit_predict(transposed1)


centroids = kmeans.cluster_centers_
print(centroids)

lables = kmeans.labels_
silhouette = silhouette_score(transposed1, lables)
# print(silhouette)
# print(transposed1)

# fig = px.parallel_coordinates(transposed1)


# colors = plt.cm.tab10.colors
# plt.figure(figsize=(10, 6))
# parallel_coordinates(transposed1, class_column='Cluster', color=colors)
# plt.show()


###This is graphing the kmeans outputs____________________________________________________________________________________________________________________________
c0 = transposed1[transposed1['Cluster'] == 0]
c1 = transposed1[transposed1['Cluster'] == 1]
c2 = transposed1[transposed1['Cluster'] == 2]
c3 = transposed1[transposed1['Cluster'] == 3]
c4 = transposed1[transposed1['Cluster'] == 4]
# parallel_coordinates(transposed1, class_column='Cluster', color=colors)
# plt.show()

parallel_coordinates(c0, class_column='Cluster', color = '#556270')
plt.ylabel('EC Percentage')
plt.show()
parallel_coordinates(c1, class_column='Cluster', color = '#4ECDC4')
plt.ylabel('EC Percentage')
plt.show()
parallel_coordinates(c2, class_column='Cluster', color = '#C7F464')
plt.ylabel('EC Percentage')
plt.show()
parallel_coordinates(c3, class_column='Cluster', color = '#00FF00')
plt.ylabel('EC Percentage')
plt.show()
parallel_coordinates(c4, class_column='Cluster', color = '#FF4500')
plt.ylabel('EC Percentage')
plt.show()


transposed1.sort_values("Cluster", axis=0, ascending=True, inplace=True, na_position='last')
print(transposed1)

