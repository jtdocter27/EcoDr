from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from sklearn.decomposition import PCA


percentages = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/all_biomes_percentage.xlsx')

transposed = percentages.T
# print(transposed)
# dropped = percentages.drop(columns=['Biome'], errors='ignore')
transposed.columns = transposed.iloc[0]
transposed1 = transposed[1:]
# print(transposed1)

# num_clusters = 50
# kmeans_tests = [KMeans(n_clusters=i, init='random', n_init=10) for i in range(1, num_clusters)]
# score = [kmeans_tests[i].fit(transposed1).score(transposed1) for i in range(len(kmeans_tests))]

# # Plot the curve
# plt.plot(range(1, num_clusters),score)
# plt.xlabel('Number of Clusters')
# plt.ylabel('Score')
# plt.title('Elbow Curve')
# plt.show()

kmeans = KMeans(init='random', n_clusters=5, n_init=10)
transposed1['Cluster'] = kmeans.fit_predict(transposed1)

print(transposed1.columns)

# fig = px.parallel_coordinates(transposed1)


import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import parallel_coordinates

colors = plt.cm.tab10.colors
plt.figure(figsize=(10, 6))
parallel_coordinates(transposed1, class_column='Cluster', color=colors)
plt.show()
