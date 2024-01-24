import numpy
import pandas as pd
import numpy as np
import os as os
from scoring import scoring
###==========================================================================================================================###
#sb_name = 'Synbio_Organism'
#_5_output = '/projects/jodo9280/EcoDr/TestCases/New_Synbio_Analysis_Output_Binary'

def ec_locator(sb_name, _5_output):
    # Reads the document that scores all genomes based on EC expression
    find_top_match = pd.read_csv(_5_output + '/Difference_Based_Comparison_Score.txt', delimiter='\t',
                                 header=0,
                                 index_col=0)
    # Finds the top match row from the difference based score that is the output of _5_. This organism is functionally most similar to the sb_name organism
    top_match_row = find_top_match.head(1).reset_index(drop=True)
  
    top_match_name = top_match_row.iloc[0, 0]   # Extracts the top match genome name GCF
    print('Top Match Found is: ', top_match_name)
    # Reads document which has EC BSM for Bacteria, Archaea, and the sb_name organism
    ec_bsm = pd.read_csv(_5_output + '/complete_binary_matrix.txt', delimiter='\t', header=0, index_col=0) #reads in a a csv to a pandas dataframe

    top_match_bsm = pd.DataFrame(ec_bsm.loc[top_match_name], columns=[top_match_name])
    print('top_match_bsm looks like ', top_match_bsm) #creates a dataframe from the given parameters
    # Sets index name of dataframe to EC Number
    top_match_bsm.index.name = 'EC-Number'
    # Finds the EC BSM for sb_name organism and transforms it into a data frame
    synbio_bsm = pd.DataFrame(ec_bsm.loc[sb_name], columns=[sb_name])
    print('synbio_bsm is looks like ', synbio_bsm)
    # Sets index name of dataframe to EC Numberpip ins
    synbio_bsm.index.name = 'EC-Number'
    # Merges two dataframes based on the EC Number rows based on outer, creating a large combined dataframe with EC BSM
    # for sb_name EC BSM and top match EC BSM
    different_ECs = pd.merge(top_match_bsm, synbio_bsm, on='EC-Number', how='outer')
    # Finds occurences where the sb_name and top match EC BSMs don't have the same binary values and extracts EC numbers
    different_ECs = different_ECs[different_ECs[sb_name] != different_ECs[top_match_name]]
    print('different_ecs look like ', different_ECs)
    # Turn on to save the list of EC numbers that are different between the two genomes and where the EC number is present
    different_ECs.to_csv(sb_name + '_different_EC_profile.txt', header=True, index=True, sep='\t')
    top_match_bsm = top_match_bsm[(top_match_bsm.loc[:, top_match_name] != 0)]
    synbio_bsm = synbio_bsm[(synbio_bsm.loc[:, sb_name] != 0)]
    print('Locating Variable EC numbers Complete')
    return different_ECs, top_match_bsm, synbio_bsm, top_match_name
#______________________________________________________________________________________________________________________________###
###Calling Script###
_to_folder = '/home/anna/Desktop/EcoGenoRisk/HazID/CompetitorFind'
# sb_name = 'Aquificota_Actinobacteria_Chimera'
sb_name = 'New_Synbio_Analysis_Output_Binary_matches.tsv'
_5_output = '/projects/jodo9280/EcoDr/TestCases/New_Synbio_Analysis_Output_Binary'
# path = '/home/anna/Desktop/EcoGenoRisk/HazID/NicheOverlap/Similar'
# sb_name = 'E_Coli_Chimera'
# sb_name = 'E_Coli_Chimera_1172_Off'
# Changes directory to local
os.chdir(_5_output)
# Sends to ec_locator() which finds the EC BSM for top match and sb_name. Returns the BSM for both organisms
[different_ECs, chassis_bsm, synbio_bsm, top_match] = ec_locator(sb_name, _5_output)
# Sends to function to compare shared InChiKeys in sb_name and top match
# Resulting matrix should be 1000-10,000 InChiKeys as this method is the "catch-all"
# Returns the shared InChiKeys without white space or duplicates
