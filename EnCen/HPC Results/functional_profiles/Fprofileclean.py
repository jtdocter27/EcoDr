##June 24th, 2024
##This script takes in the functional profile and turns it into a list of percentages within the biome. 
import pandas as pd
import numpy as np
###______________________________________________________________________________________________________________
profile = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/HPC Results/functional_profiles/Activated_Sludge_Metagenome_functional_profile', header=None)

funcprof = profile.iloc[:,0].str.split(' ', expand=True) #this is the fancy bit of code that takes all the rows and first column (this is only one column in this dataframe to begin with) and splits each element by the space character. Expand = true puts each value in it's own column

# print(funcprof.head())
print('total rows are: ', len(funcprof))
print('total columns are:', funcprof.shape[1])

funcprof.columns = funcprof.iloc[0] #assigns the first row (iloc[0] to the columns of the dataframe)
funcprof = funcprof[1:] #creates a new dataframe from the second row onward. 

for col in funcprof.columns[1:]:
    funcprof[col] = pd.to_numeric(funcprof[col]) #converts all the dtype=object data to numbers. This is because pd.read_csv read the dataframe in as a string. 

sum = funcprof.iloc[:, 1:].sum() #sums all rows, second column onward. 

row = len(funcprof) -1 #just get's the amount of rows minus the summed row. 
# print(row)
funcprof.loc[len(funcprof)] = sum #adds the summed row onto the dataframe

percentage = funcprof.iloc[1373].div(row) #divides the summed row by the amount of rows, i.e. finding the percentage of each enzyme. 
print(type(percentage))

final = pd.DataFrame(percentage) #turns numpy array into dataframe...why this is a numpy array, I don't know. 
final.columns = final.iloc[0] #turns the first row into the column names 
final = final[1:] #new dataframe is second row onward. 
# final = final.dropna()
final.columns = ['Percentage'] #turns the column into a percentage 
final = final.mul(100) #multiplies by 100 to get out of decimal form 
final = final.sort_values(by=['Percentage'], ascending=False) #sort the column percentage from high to low 
if final.iloc[0].isnull().all(): #gets rid of the weird first row that is null. 
    final = final.drop(0)
print(final)

