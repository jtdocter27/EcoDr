import pandas as pd
import numpy as np

profile = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC Results/functional_profiles/Activated_Sludge_Metagenome_functional_profile', header=None)

funcprof = profile.iloc[:,0].str.split(' ', expand=True)

# print(funcprof.head())
print('total rows are: ', len(funcprof))
print('total columns are:', funcprof.shape[1])

funcprof.columns = funcprof.iloc[0]
funcprof = funcprof[1:]
# print(funcprof)
# print(funcprof.iloc[0])#This tells me that the first column is the index currently. This outputs the first row
# sum = funcprof.sum(axis=1)
# print(funcprof.dtypes)

for col in funcprof.columns[1:]:
    funcprof[col] = pd.to_numeric(funcprof[col])

sum = funcprof.iloc[:, 1:].sum()
# print(sum)
row = len(funcprof) -1
print(row)
funcprof.loc[len(funcprof)] = sum
# percentage = funcprof[1374].div(row)
percentage = funcprof.iloc[1373].div(row)
# print(percentage)


final = pd.DataFrame(percentage)
final.columns = final.iloc[0]
final = final[1:]
final = final.dropna()
final.columns = ['Percentage']
final = final.mul(100)
final = final.sort_values(by=['Percentage'], ascending=False)
if final.iloc[0].isnull().all():
    final = final.drop(0)
final = final.reset_index(drop=True)
print(final)

