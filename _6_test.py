import numpy
import pandas as pd
import numpy as np
import os as os
from scoring import scoring
###==========================================================================================================================###
#sb_name = 'Synbio_Organism'
#_5_output = '/projects/jodo9280/EcoDr/TestCases/New_Synbio_Analysis_Output_Binary'

def ec_comparison(sb_name, _5_output):
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
    #print('top_match_bsm looks like ', top_match_bsm) #creates a dataframe from the given parameters
    # Sets index name of dataframe to EC Number
    top_match_bsm.index.name = 'EC-Number'
    # Finds the EC BSM for sb_name organism and transforms it into a data frame
    synbio_bsm = pd.DataFrame(ec_bsm.loc[sb_name], columns=[sb_name])
    #print('synbio_bsm is looks like ', synbio_bsm)
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

    top_match_bsm = top_match_bsm[(top_match_bsm.loc[:, top_match_name] != 0)] #this filters out all the zeroes from the top match dataframe
    print('top match bsm is, ', top_match_bsm)

    synbio_bsm = synbio_bsm[(synbio_bsm.loc[:, sb_name] != 0)] #this also filters out all the zeroes from the synbio match dataframe
    print('synbio_bsm is ', synbio_bsm)


    print('Locating Variable EC numbers Complete')
    return different_ECs, top_match_bsm, synbio_bsm, top_match_name
#_______________________________________________________________________________#_______________________________________________###
#sb_name = 'New_Synbio_Analysis_Output_Binary_matches.tsv'
#_to_folder = '/projects/jodo9280/EcoDr/EcoDr/Competitor_Find'
#top_match_bsm = Dataframe with all of the EC's present on the top match 
#synbio_bsm = Dataframe with all of EC's present on the Synbio organism 

def substrate_changes_synbio_v_topmatch(_to_folder, top_match_bsm, synbio_bsm):
    os.chdir('/projects/jodo9280/EcoDr/EcoDr/Competitor_Find')
    # Opens MetaCyc list of all reactions
    metacyc_all_rxns = pd.read_csv(_to_folder + '/All-reactions-of-MetaCyc.txt',
                                   delimiter='\t', header=0, index_col=0) #reads in this file, will need to locate on work computer. 
    # Converts into database
    metacyc_all_rxns = pd.DataFrame(metacyc_all_rxns)
    #print('Metacyc_all_rxns looks like ', metacyc_all_rxns.head())

    metacyc_all_rxns.columns = ['EC-Number', 'Substrates', 'Substrates InChI-Key', 'Reactants',
                                'Reactants InChI-Key', 'Products', 'Products InChI-Key'] #this renames the columns in the dataframe starting with EC-Number... I don't know why. 
    print('metacyc_all_rxns columns looks like\n\n', metacyc_all_rxns.columns)
    #print('Here is the reactants Inchi-key column ', metacyc_all_rxns['Reactants InChI-Key'])

    metacyc_all_rxns['EC-Number'] = metacyc_all_rxns['EC-Number'].str.replace('EC-', '', regex=False) #gets rid of EC- in the EC-number column, so we are left with just the actually number.
    # Merges based on EC number to create a list of reactions/substrates occurring in top match
    #Top_match Dataframe Creation__________________________________
    top_match_rxns = pd.merge(top_match_bsm, metacyc_all_rxns, on='EC-Number', how='inner')
    print('top_match_rxns looks like :\n', top_match_rxns.head())
    #print(top_match_rxns['Reactants InChI-Key'])

    # Turn on to save the list of reactants found in top match
    top_match_rxns.to_csv('_top_match_all_rxns.txt', header=True, index=True, sep='\t') #outputs a csv from top_match_reactions
    # Isolates the InChI Key column and splits the column based on // to isolate all substrates for top match
    top_match_InChI_Key = pd.DataFrame(top_match_rxns['Reactants InChI-Key'].astype(str).str.split('//', expand=True)) #makes a new dataframe 
    top_match_one_col = to_one_column(top_match_InChI_Key) #just some data processing 
    top_match_one_col.to_csv('_top_match_only_reactants.txt', header=True, index=True, sep='\t')
    
    ##Synbio DataFrame Creation_______________________________________
    # Merges based on EC number to create a list of reactions/substrates occurring in synbio
    synbio_rxns = pd.merge(synbio_bsm, metacyc_all_rxns, on='EC-Number', how='inner')
    # Merges the synbio binary summary matrix with the metacyc list to find the InChI-Key lists
    # Splits InChI-Keys based on the '//' separator
    synbio_InChI_Key = pd.DataFrame(synbio_rxns['Reactants InChI-Key'].astype(str).str.split('//', expand=True))
    synbio_one_col = to_one_column(synbio_InChI_Key)
    # Turn on to save the list of substrates found in synbio
    synbio_one_col.to_csv('_synbio_only_reactants.txt', header=True, index= True, sep='\t')
    # Isolates the InChI Key column and splits the column based on // to isolate all substrates for synbio
    # Creates an array of InChI Keys of substrates that can be found in both organisms, saves the array as index

    ##Combining Synbio and Top match Reactant Dtaframes
    Combined_InChI_Key = pd.merge(synbio_one_col, top_match_one_col, on='InChI-Key', how='inner').reset_index(drop=True) #'inner' keeps only the common values between the two dataframes. This is important. 
    Combined_InChI_Key = Combined_InChI_Key.dropna(how='any')
    print('Synbio and Top Match Organism Substrate DataFrames Have Merged')
    # Returns the InChI Key names by referencing the index
    # Converts array into a single column list
    # Removes any spaces
    Combined_InChI_Key['InChI-Key'] = Combined_InChI_Key['InChI-Key'].str.strip()
    # Finds unique InChI Keys in the list
    unique_top_match_InChI_Key = Combined_InChI_Key['InChI-Key'].drop_duplicates()
    unique_top_match_InChI_Key.reset_index(drop=True)
    # Saves list of InChI Keys
    unique_top_match_InChI_Key = pd.DataFrame(unique_top_match_InChI_Key, columns=['InChI-Key'])

    # Removes the common InChI-Keys such as proton, ATP, and saves the list
    top_match_inchi_keys_translated = relevant_compounds(unique_top_match_InChI_Key) #takes in the dataframe and gets rid of common compounds like water. 
    top_match_inchi_keys_translated.to_csv('_synbio_x_topmatch_inchikey.txt', header=True, index=True, sep='\t')
    # unique_top_match_InChI_Key.to_csv(sb_name+'_synbiovschassis_inchikey.txt', header=True, index= True, sep='\t')
    print('Top Match vs. Synbio InChI Key Substrates Analysis Is Complete')
    return unique_top_match_InChI_Key
###_____________________________________________________________________________________________________________________________###
def to_one_column(df):
    all_values = []
    for column in df:
        # Converts every line to a list and adds it to itself
        pathway_list = df[column].tolist()
        all_values += pathway_list
    one_col = pd.DataFrame(all_values, columns=['InChI-Key'])
    # Removes all None, blank spaces with NaN
    one_col['InChI-Key'].replace('None', np.nan)
    one_col['InChI-Key'].replace('', np.nan)
    # Drops all NaN types
    one_col.dropna()
    # Converts all lines into string and removes white space when present
    one_col['InChI-Key'].astype(str).str.strip()
    # Removes any duplicates
    one_col['InChI-Key'].drop_duplicates()
    # Resets the index in single column
    one_col.reset_index(drop=True)
    print(one_col)
    return one_col
###______________________________________________________________________________________________________________________________###
def relevant_compounds(df):
    # Finds the indexes where InChiKey for water are present
    index_water = df[df['InChI-Key'] == 'InChIKey=XLYOFNOQVPJJNP-UHFFFAOYSA-N'].index
    # Finds the indexes where InChiKey for NADPH are present
    index_NADPH = df[df['InChI-Key'] == 'InChIKey=ACFIXJIJDZMPPO-NNYOXOHSSA-J'].index
    # Finds the indexes where InChiKey for NADP are present
    index_NADP = df[df['InChI-Key'] == 'InChIKey=XJLXINKUBYWONI-NNYOXOHSSA-K'].index
    # Finds the indexes where InChiKey for Proton are present
    index_proton = df[df['InChI-Key'] == 'InChIKey=GPRLSGONYQIRFK-UHFFFAOYSA-N'].index
    # Removes row if InChIKEy for water is present
    df.drop(index_water, inplace=True)
    # Removes row if InChIKey for NADPH is present
    df.drop(index_NADPH, inplace=True)
    # Removes row if InChIKey for NADP is present
    df.drop(index_NADP, inplace=True)
    # Removes row if InChIKey for Proton is present
    df.drop(index_proton, inplace=True)
    # Resets index
    df.reset_index(drop=True)
    # Returns list of relevant InChiKeys
    return df
####----------------------------------------------------------------------------------------###
def inchikey_to_conventional_names(df):
    key = pd.read_csv(_to_folder + '/InchiKeystoCompoundNames.txt', delimiter='\t', header=0, index_col=None)
    translated_inchikeys = pd.merge(df, key, on='InChI-Key', how='left')
    translated_inchikeys = translated_inchikeys.dropna()
    translated_inchikeys.to_csv('InchiKey_names.txt', header=True, index=True, sep='\t') #this was originally in the running script, moved here for conciseness 
    print('Translated Inchikeys Look like :\n', translated_inchikeys.head())
    return translated_inchikeys
###__________________________________________________________________________________________####
#_to_folder = '/projects/jodo9280/EcoDr/EcoDr/Competitor_Find'
def mutualism1_modified_pathway(_to_folder, top_match_bsm, synbio_bsm):
    # Opens MetaCyc list of all reactions
    metacyc_all_rxns = pd.read_csv(_to_folder + '/All-reactions-of-MetaCyc.txt',
                                   delimiter='\t', header=0, index_col=0)
    # Converts into database
    metacyc_all_rxns = pd.DataFrame(metacyc_all_rxns)
    print('Old column names\n', metacyc_all_rxns.columns)
    metacyc_all_rxns.columns = ['EC-Number', 'Substrates', 'Substrates InChI-Key', 'Reactants',
                                'Reactants InChI-Key', 'Products', 'Products InChI-Key']
    print('New Columns Names\n', metacyc_all_rxns.columns)

    # String processing of dataframe by removing 'EC-' from the start of the EC number
    print('Here is the reactants column\n', metacyc_all_rxns['Reactants InChI-Key'])
    metacyc_all_rxns['EC-Number'] = metacyc_all_rxns['EC-Number'].str.replace('EC-', '', regex=False)
    # Merges based on EC number to create a list of reactions/substrates occurring in top match
    top_match_rxns = pd.merge(top_match_bsm, metacyc_all_rxns, on='EC-Number', how='inner')
    print('This is top_match_rxns\n', top_match_rxns.head())
    #print(top_match_rxns['Reactants InChI-Key'])

    # Turn on to save the list of substrates found in top match
    top_match_rxns.to_csv('topmatch_' + sb_name + '_chassis_all_rxns.txt', header=True, index=True, sep='\t')
    # Isolates the InChI Key column and splits the column based on // to isolate all substrates for top match
    chassis_InChI_Key = pd.DataFrame(top_match_rxns['Products InChI-Key'].astype(str).str.split('//', expand=True))
    chassis_one_col = to_one_column(chassis_InChI_Key)
    chassis_one_col.to_csv(sb_name + '_chassis_all_rxns.txt', header=True, index=True, sep='\t')
    # Merges based on EC number to create a list of reactions/substrates occurring in synbio
    synbio_rxns = pd.merge(synbio_bsm, metacyc_all_rxns, on='EC-Number', how='inner')
    # Merges the synbio binary summary matrix with the metacyc list to find the InChI-Key lists
    # Splits InChI-Keys based on the '//' separator
    synbio_InChI_Key = pd.DataFrame(synbio_rxns['Reactants InChI-Key'].astype(str).str.split('//', expand=True))
    synbio_one_col = to_one_column(synbio_InChI_Key)
    # Turn on to save the list of substrates found in synbio
    # synbio_one_col.to_csv(sb_name+'_synbio_all_rxns.txt', header=True, index= True, sep='\t')
    # Isolates the InChI Key column and splits the column based on // to isolate all substrates for synbio
    # Creates an array of InChI Keys of substrates that can be found in both organisms, saves the array as index
    shared_InChI_Key = pd.merge(synbio_one_col, chassis_one_col, on='InChI-Key', how='inner').reset_index(drop=True)
    print('I have merged')
    # Returns the InChI Key names by referencing the index
    # Converts array into a single column list
    # Removes any spaces
    shared_InChI_Key['InChI-Key'] = shared_InChI_Key['InChI-Key'].str.strip()
    # Finds unique InChI Keys in the list
    unique_chassis_InChI_Key = shared_InChI_Key['InChI-Key'].drop_duplicates()
    unique_chassis_InChI_Key.reset_index(drop=True)
    # Saves list of InChI Keys
    unique_chassis_InChI_Key = pd.DataFrame(unique_chassis_InChI_Key, columns=['InChI-Key'])
    # Removes the common InChI-Keys such as proton, ATP, and saves the list
    chassis_inchi_keys_translated = relevant_compounds(unique_chassis_InChI_Key)
    chassis_inchi_keys_translated.to_csv(sb_name + 'mutualism1.txt', header=True, index=True, sep='\t')
    return chassis_inchi_keys_translated

###Calling Script###
_to_folder = '/projects/jodo9280/EcoDr/EcoDr/Competitor_Find'
# sb_name = 'Aquificota_Actinobacteria_Chimera'
sb_name = 'New_Synbio_Analysis_Output_Binary_matches.tsv'
#file_name = 'InChiKey'
_5_output = '/projects/jodo9280/EcoDr/TestCases/New_Synbio_Analysis_Output_Binary'
# path = '/home/anna/Desktop/EcoGenoRisk/HazID/NicheOverlap/Similar'
# sb_name = 'E_Coli_Chimera'
# sb_name = 'E_Coli_Chimera_1172_Off'
# Changes directory to local
os.chdir(_5_output)
# Sends to ec_locator() which finds the EC BSM for top match and sb_name. Returns the BSM for both organisms
[different_ECs, top_match_bsm, synbio_bsm, top_match] = ec_comparison(sb_name, _5_output)
# Sends to function to compare shared InChiKeys in sb_name and top match
# Resulting matrix should be 1000-10,000 InChiKeys as this method is the "catch-all"
# Returns the shared InChiKeys without white space or duplicates
#individual_genome_rxns = substrate_changes_synbio_v_chassis(synbio, _to_folder, synbio_bsm, top_match_bsm)
individual_genome_rxns = substrate_changes_synbio_v_topmatch(_to_folder, synbio_bsm, top_match_bsm)
translated_individual_rxns = inchikey_to_conventional_names(individual_genome_rxns)
mutualism1 = mutualism1_modified_pathway(_to_folder, top_match_bsm,synbio_bsm)