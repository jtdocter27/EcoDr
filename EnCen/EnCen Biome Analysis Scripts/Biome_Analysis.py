#July 18th, 2024
#This is a script that will take in the biome output dataframe from fprofileclean.py and...
#1) Screen for just Topmatch functions
#2) Screen for lost functions, i.e. which ones the topmatch has that the synbio does not 
#3) Characterize %shift in biome function
#4) Identify lost functions (those that occur only once) 
import pandas as pd 


def top_match_presence_screen(biome_full_dataframe):
    biome_full_pd = pd.read_excel(biome_full_dataframe, header=0, dtype={'Top Match Presence/Absence': int})
    top_match_only = biome_full_pd[biome_full_pd['Top Match Presence/Absence'] == 1]
    return top_match_only

def lost_functions(top_match_dataframe): #This assumes that all functions that are lost are the ones that the synbio doesn't have that the top match does when it is replaced. 
    lost_functions = top_match_dataframe[top_match_dataframe['Synbio Presence/Absence'] == 0]
    return lost_functions

def percent_shift(lost_functions_df):
    percent_loss = 1/1373 #this is the % loss of losing one instance of the enzyme, the ratio given is one enzyme per bins. 
    lost_functions_df.iloc[:, 'Percentages After Loss'] = lost_functions_df['Percentage'] - percent_loss
    return lost_functions_df



biome_full_dataframe = '/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/EnCen/Biome Synbio Top Match EC Comparison.xlsx'
top_match_dataframe = top_match_presence_screen(biome_full_dataframe)
# top_match_dataframe.to_excel('Only Present Enzyme Biome Synbio Top Match EC Comparison.xlsx', index=False)
lost_functions_df = lost_functions(top_match_dataframe)
# lost_functions_df.to_excel('Lost_Functions.xlsx', index=False)
percent_shift_df = percent_shift(lost_functions_df)
percent_shift_df.to_excel('percent shift after functional loss.xlsx', index=False)
