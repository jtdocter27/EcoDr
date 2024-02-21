import pandas as pd
import pubchempy as pcp
import numpy as np
import os as os
from itertools import chain
Yellow = "\033[33m"

path = '/projects/jodo9280/EcoDr/EcoDr/Poisinhibitor'
all_rxns_doc = '/projects/jodo9280/EcoDr/EcoDr/Competitor_Find/All-reactions-of-MetaCyc.txt'
inhibited_org = '/projects/jodo9280/EcoDr/EcoDr/Poisinhibitor/prokaryote_inhibitor_list.csv'
inchikey_compound_name = '/projects/jodo9280/EcoDr/EcoDr/Competitor_Find/InchiKeystoCompoundNames.txt'


def similarity_search(path, all_rxns_doc):
    os.chdir(path) #this is just the path to the PoisInhibitor File. 
    inhibitor = input('Enter your inhibitors InChI-Key Code : \n')
    #'LRHPLDYGYMQRHN-UHFFFAOYSA-N'
    print('Enter number of similar structures desired')
    print("Note, as a user, this is how specific or general you want your inhibitor search to be. \n\n 1 indicates you have high confidence that this ligand-enzyme match will be in the database. \n A value of 50 likely affords a general search based on functional profiles.")
    print("It is highly recommended that you inspect the molecular form of the final inhibitor to determine structural similarity to your target compound.")
    n = input('Specify the Amount of Records you Would Like to Retrieve From PubChem:\n')
    print('This is Orcrist, the Golbin Cleaver, a famous blade, made by the high elves of the west, my kin.\n May it serve you well [hands back to thorin]')
    status = 1
    analogous = []
    try:
        inhibitor_info = pcp.get_compounds(inhibitor, 'inchikey', as_dataframe=True)
        #pcp.get_compounds(identifier, type of identifier, creates an object as a pandas dataframe (True))
        inhibitor_cid = inhibitor_info.index[0].astype('str') #This just takes the CID 
        #print('Inhibitor is :\n', inhibitor_info)
    except:
        print('Unable to find structure')
        status = 0
    try:
        print('Finding similar structures...')
        similar = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='similarity', listkey_count=n)
        #print('Similair Structure is :', similar)
    except:
        print('Unable to find similar structures')
        status = 0
    try:
        print('Finding substructures...')
        substructure = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='substructure', listkey_count=n)
        #print('Substructure is :', substructure)
    except:
        print('Unable to find substructures')
        status = 0
    try:
        print('Finding superstructures...')
        superstructure = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='superstructure', listkey_count=n)
        #print('Superstructure is :', superstructure)
    except:
        print('Unable to find superstructure')
        status = 0
    if status == 1:
        analogs = similar + substructure + superstructure
        #print('analogs are :\n', analogs)
        inchikeys = []
        for compound in analogs:
            inchikeys.append(str(compound.inchikey))
        analogous = pd.DataFrame({'Similar_Structure InchiKeys': inchikeys})
        analogous.drop_duplicates()
        analogous.reset_index(drop=True)
        analogous.to_csv('similar_compounds.txt')
    return analogous, status

def inchikey_translation(inhibited_org, inchikey_compound_name):
    # Opens the BRENDA curated list of organisms and their inhibitors
    # List was created by searching for inhibitors for prokaryotes 
    list_of_orgs_inhibited = pd.read_csv(inhibited_org, delimiter='\t')
    # Creates column names
    list_of_orgs_inhibited.columns = ['EC Number', 'Enzyme Name', 'Inhibitor Compound Name', '-', 'Species', '-', '-',
                                      'Primary accession Number']
    # Opens BioCyc curated list of compounds and their inchikeys
    comp_to_inchikey = pd.read_csv(inchikey_compound_name, delimiter='\t')
    comp_to_inchikey.columns = ['BioCyc Id', 'InChI-Key']
    # Converts the common names of compounds to all lower case (ex: CU 2+ --> cu 2+)
    list_of_orgs_inhibited['Inhibitor Compound Name'] = list_of_orgs_inhibited['Inhibitor Compound Name'].str.lower()
    comp_to_inchikey['BioCyc Id'] = comp_to_inchikey['BioCyc Id'].str.lower()
    # Merges two dataframes to create a list of cummulative list of compounds, their InChiKeys, and organisms inhibited
    inhibitors_translated = pd.merge(list_of_orgs_inhibited, comp_to_inchikey, how='inner',
                                     left_on='Inhibitor Compound Name',
                                     right_on='BioCyc Id')
    print('Inhibitors Translated Looks like :\n', inhibitors_translated)
    inhibitors_translated['InChI-Key'] = inhibitors_translated['InChI-Key'].str.replace('InChIKey=', '')
    # Saves the dataframe to a csv
    inhibitors_translated.to_csv('translated_inchikey.txt', header=True, index=True, sep='\t')
    # Subsets the data frame to select only the InChI-Key column and EC number
    # Overall dataframe is EC numbers that are inhibited along with their inhibitors InChI-Key notation
    ec_inchikeys_inhibited = inhibitors_translated[['EC Number', 'InChI-Key']]
    ec_inchikeys_inhibited.to_csv('ec_inchikey_inhibited.txt', sep='\t')
    print('It does not do to leave a live dragon out of your calculations, if you live near him')
    return ec_inchikeys_inhibited


#ec_inchikeys_inhibited is the list of ec's and inchikeys generated from the previous definition
#analogous is similair_compounds.txt Inchikeys
def vulnerable_pop(ec_inchikeys_inhibited, analogous):
    # Merges the EC number. inhibitor in InChiKey notation, and organism species name with the taxonomy dataset
    combined_binary = pd.read_csv(
        '/projects/jodo9280/EcoDr/TestCases/New_Synbio_Analysis_Output_Binary/complete_binary_matrix.txt', header=0,
        index_col=0, sep='\t')
    # Creates a list of all EC numbers
    current_working_ec = pd.DataFrame(combined_binary.columns)
    print(Yellow, 'Current Working EC is:\n', current_working_ec.head(5))
    current_working_ec.columns = ['Current Working ECs']
    # Merges analogous inhibitor list with list of EC numbers that are inhibited with their inhibitors
    # Overall result is EC number inhibited, Inhibitor Compound Name, Inhibitor InChI-Key name
    inhibited_by_sim_compounds_found = pd.merge(ec_inchikeys_inhibited, analogous, how='inner', left_on='InChI-Key',
                                                right_on='Similar_Structure Inchikeys') #Merge the two dataframes on the overlapping InchiKeys
    print(Yellow,'inhibited_by_sim_compound_found is:', inhibited_by_sim_compounds_found.head(10))
    # Isolates only the EC number, InChiKey names
    inhibited_by_sim_compounds_abridged = inhibited_by_sim_compounds_found[['EC Number', 'InChI-Key']]
    # Saves the specified dataframe, isolates by column names
    inhibited_by_sim_compounds_abridged.to_csv('org_inhibited_in_GCF_notation.txt')
    # Creates a list of all unique EC numbers inhibited
    ec_numbers_inhibited = inhibited_by_sim_compounds_abridged['EC Number'].drop_duplicates()
    print(Yellow,'Total number of unique EC numbers inhibited is: ', ec_numbers_inhibited.shape)
    # Creates a list of EC numbers that are present in both the EC BSM and the inhibitors list in ec_numbers_inhibited




    # This addresses if new EC numbers are listed in the BRENDA dataset but not in the EC BSM
    ec_list_present = pd.merge(ec_numbers_inhibited, current_working_ec, how='inner', left_on='EC Number',
                               right_on='Current Working ECs')
    ec_list_present.to_csv('ec_inhibited.txt', sep='\t')
    # Creates summary dataframes
    for_particular_ec = pd.DataFrame(columns=['PoisInhibitor'])
    genomes = []
    # Loops through the EC numbers inhibited
    
    
    for ec in ec_list_present['EC Number']:
        print(ec)
        if ec == 'EC Number':
            print(Yellow,'EC Already Present')
        else:
            # If 1 is present in the EC column, isolate the rows with the present enzyme
            # Return a list of genomes that have the EC numebr present
            found_orgs = combined_binary[combined_binary.loc[:, ec] == 1].index.tolist() #looks for all EC's that are 1 and then takes the associated genome and puts it into a list. 
            print('Number of genomes that contain the enzyme: ',
                  combined_binary[combined_binary.loc[:, ec] == 1].shape[0])
            print(Yellow, "Found Orgs are:\n", found_orgs)
            if len(found_orgs) != 0:
                # Create a dataframe of all genomes that have the EC number inhibited
                new_df = pd.DataFrame(found_orgs, columns=[ec])
                # Vertically add the dataframe to the summary dataframe
                for_particular_ec = pd.concat([for_particular_ec, new_df], axis=1)
                # Add the genomes to a list
                genomes.append(found_orgs)
    # Opens the taxonomy spreadsheet
    taxonomy = pd.read_csv('/projects/jodo9280/EcoDr/taxonomy_2023_6_27.tsv', header=0,
                           index_col=0, sep='\t')
    taxonomy.columns = ['Name_of_Genome', 'Domain', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    one_dim_genome = list(chain.from_iterable(genomes)) #flattens a nested list in genomes into a single list. 
    df_genomes_inhibited = pd.DataFrame(one_dim_genome)
    df_genomes_inhibited.columns = ['Inhibited_Genomes']
    # Merges the GCF organisms with their taxonomic lineage
    labelled_inhibited_genomes = pd.merge(taxonomy, df_genomes_inhibited, left_on='Name_of_Genome',
                                          right_on='Inhibited_Genomes', how='inner')
    print(Yellow, "lebbeled_inhibited_genomes \n", labelled_inhibited_genomes)
    # Isolates the Species column and drops any duplicates, rows with NaN, empty rows, or rows with ,
    labelled_inhibited_genomes['Species'] = labelled_inhibited_genomes['Species'].drop_duplicates()
    labelled_inhibited_genomes.replace('', float('NaN'), inplace=True)
    labelled_inhibited_genomes.replace(',', float('NaN'), inplace=True)
    unique_labelled = labelled_inhibited_genomes['Species'].dropna(axis=0)
    unique_labelled.to_csv('labelled_inhibited_species.txt')
    return for_particular_ec, genomes


#This chunk just finds the number of unique genomes in the previously generated dataframe and the number of unique EC's
def scoring(inhibited_organisms_by_ec, genomes):
    
    # Converts list of all genomes in a numpy array
    as_array_genomes = np.array(genomes, dtype=object)
    # Finds the number of unique genomes
    unique_genomes = np.unique(as_array_genomes)
    print('Number of unique genomes is: ', unique_genomes.size)
    # Counts number of columns in the summary dataframe
    number_of_ec = inhibited_organisms_by_ec.shape[1] - 1
    print('Number of unique EC is: ', number_of_ec)
    inhibited_organisms_by_ec.to_csv('inhibited_organisms_by_ec.txt')
    return



##Test Script, Functionaly______________________________________________________________________________________
[analogous, status] = similarity_search(path, all_rxns_doc)
if status == 1:
    ec_inchikeys_inhibited = inchikey_translation(inhibited_org, inchikey_compound_name)
    [for_particular_ec, genomes] = vulnerable_pop(ec_inchikeys_inhibited, analogous)
    scoring(for_particular_ec, genomes)
else:
    print('Try again with fewer number of similar structures or with a different InChI-Key')