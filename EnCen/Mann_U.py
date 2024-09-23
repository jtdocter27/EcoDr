from scipy import stats
from scipy.stats import mannwhitneyu
import numpy as np 
import pandas as pd

##Converting Everything into lists__________________________________________________________________________________________________________________________________________________________________________________
acs = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC and Functional Profile Results/Activated_Sludge/synbio_inputs_and_outputs/Act_Sludge_Absolute_Difference_Comparison_Score.txt', delimiter = '\t')
score = pd.DataFrame(acs['Difference Score'])
list_acs = score['Difference Score'].tolist()

ag = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC and Functional Profile Results/Agricultural Bulk Soil/Bulk_Soil_Absolute_Difference_Comparison_Score.txt', delimiter = '\t')
score_ag = pd.DataFrame(ag['Difference Score'])
list_ag = score_ag['Difference Score'].tolist()

cow = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC and Functional Profile Results/Cow Rumen/Cow_Rumen_Absolute_Difference_Comparison_Score.txt', delimiter = '\t')
score_cow = pd.DataFrame(cow['Difference Score'])
list_cow = score_cow['Difference Score'].tolist()

lake = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC and Functional Profile Results/Lake Sediment/Lake_Sediment_Absolute_Difference_Comparison_Score.txt', delimiter = '\t')
score_lake = pd.DataFrame(lake['Difference Score'])
list_lake = score_lake['Difference Score'].tolist()

river = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC and Functional Profile Results/River_Sediment/River_Sediment)Absolute_Difference_Comparison_Score.txt', delimiter= '\t')
score_river = pd.DataFrame(river['Difference Score'])
list_river = score_river['Difference Score'].tolist()

##Stats test_____________________________________________________________________________________________________________________________________________________________________________________________________
stat, p_value = mannwhitneyu(list_river, list_cow)

print('Statistics=%.2f, p=%.2f' % (stat, p_value)) 
# Level of significance 
alpha = 0.05
# conclusion 
if p_value < alpha: 
    print('Reject Null Hypothesis (Significant difference between two samples)') 
else: 
    print('Do not Reject Null Hypothesis (No significant difference between two samples)')


