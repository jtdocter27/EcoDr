import pandas as pd
import scipy.stats as stats
from scipy.stats import hypergeom
from sklearn.cluster import KMeans
from statsmodels.stats.multitest import multipletests

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


EC_per_cluster = reset2.groupby('Cluster')['EC'].value_counts()

print(EC_per_cluster)

total_EC_class = EC_per_cluster.groupby('EC').sum()
print(total_EC_class)

total_cluster_count = EC_per_cluster.groupby('Cluster').sum()
print(total_cluster_count)

# N=8370 #total population (Total EC's)
# K=2560 #Number of successes in the population (Total EC in the population)
# n=816 #Sample size (number of total ECs in the cluster)
# k=249 #Sample Successes (number of specific EC's in the cluster)

# p_value_1 = 1- stats.hypergeom.cdf(k-1, N, K, n)
# print(p_value_1)

#Cluster 0_________________________________________________________________________
N=8370 #total population (Total EC's) #Unchaged 
# K=2560 #Number of successes in the population (Total EC in the population) #changes
n=816 #Sample size (number of total ECs in the cluster) #Changes per cluster
# k=249 #Sample Successes (number of specific EC's in the cluster) #changes

K = [2560, 2287, 1806, 900, 347, 271, 98]
k = [249, 190, 188, 94, 44, 26, 25]

n2 = len(k)

def multi_p(N, n, K, k):
    p_values_final = []
    for i in range(n2):
        k2 = k[i]
        K2 = K[i]
        p_value = 1 - hypergeom.cdf(k2 -1, N, K2, n)
        # if p_value < 0.05: 
        p_values_final.append(p_value)
    return p_values_final

cluster_0_p_values = multi_p(N, n, K, k)
print('Cluster 0 p_values: ', cluster_0_p_values, '\n')


#Cluster 1_____________________________________________________________________________
n= 6720
k = [2187, 1845, 1472, 738, 259, 179, 40]


cluster_1_p_values = multi_p(N, n, K, k)
print('Cluster 1 p_values: ', cluster_1_p_values, '\n')

#Cluster 2_________________________________________________________________________________
n = 328
k = [92, 86, 68, 30, 20, 18, 14]


cluster_2_p_values = multi_p(N, n, K, k)
print('Cluster 2 p_values: ', cluster_2_p_values, '\n')

#Cluster 3___________________________________________________________________________________
n = 177
k = [62, 35, 31, 16, 15, 14, 4]


cluster_3_p_values = multi_p(N, n, K, k)
print('Cluster 3 p_values: ', cluster_3_p_values, '\n')

#Cluster 4_____________________________________________________________________________________
n = 228
k= [98, 40, 29, 24, 17, 11, 9]


cluster_4_p_values = multi_p(N, n, K, k)
print('Cluster 4 p_values: ', cluster_4_p_values, '\n')

#Bonferroni_Correction________________________________________________________________________________________
all_p_values = cluster_0_p_values + cluster_1_p_values + cluster_2_p_values + cluster_3_p_values +cluster_4_p_values
print(all_p_values)

b_rejected, b_corrected, _,_ = multipletests(all_p_values, alpha = 0.05, method='bonferroni')

print('rejected: ', b_rejected)
print('adjusted: ', b_corrected, '\n')

cluster_0_corrected = b_corrected[0:7]
print('Cluster 0 Correct: ', cluster_0_corrected, '\n')

cluster_1_corrected = b_corrected[7:14]
print('Cluster 1 Correct: ', cluster_1_corrected, '\n')


cluster_2_corrected = b_corrected[14:21]
print('Cluster 2 Correct: ', cluster_2_corrected, '\n')


cluster_3_corrected = b_corrected[21:28]
print('Cluster 3 Correct: ', cluster_3_corrected, '\n')


cluster_4_corrected = b_corrected[28:35]
print('Cluster 4 Correct: ', cluster_4_corrected, '\n')

print(len(all_p_values))

