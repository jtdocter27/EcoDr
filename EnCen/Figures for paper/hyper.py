import pandas as pd
from scipy.stats import hypergeom
from sklearn.cluster import KMeans

percentages = pd.read_excel('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/all_biomes_percentage.xlsx')

transposed = percentages.T
# print(transposed)
# dropped = percentages.drop(columns=['Biome'], errors='ignore')
transposed.columns = transposed.iloc[0]
transposed1 = transposed[1:]



num_clusters = 50
kmeans_tests = [KMeans(n_clusters=i, init='random', n_init=10) for i in range(1, num_clusters)]
score = [kmeans_tests[i].fit(transposed1).score(transposed1) for i in range(len(kmeans_tests))]


kmeans = KMeans(init='random', n_clusters=5, n_init=10)
transposed1['Cluster'] = kmeans.fit_predict(transposed1)

new = transposed1

new.sort_values("Cluster", axis=0, ascending=True, inplace=True)
# print(new)

zero = (new.loc[(new['Cluster'] == 0)])
print(zero)

# zero = zero.reset_index()
# strings = zero['index'].astype(str)

# count_sravan = strings.value_counts().get('2_', 0)

##To-Do
#- Somehow turn the EC's into ints...probably need some regular expressiosn or something to parse these
#- count instances 
#- instances will be "successes" in distribution 