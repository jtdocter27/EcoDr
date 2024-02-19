import pandas as pd
import pubchempy as pcp
import numpy as np
import os as os
from itertools import chain

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

[analogous, status] = similarity_search(path, all_rxns_doc)
if status == 1:
    ec_inchikeys_inhibited = inchikey_translation(inhibited_org, inchikey_compound_name)
    #[for_particular_ec, genomes] = vulnerable_pop(ec_inchikeys_inhibited, analogous)
    #scoring(for_particular_ec, genomes)
else:
    print('Try again with fewer number of similar structures or with a different InChI-Key')
