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
    #print('Enter your inhibitors InChI-Key code: ')
    inhibitor = 'LRHPLDYGYMQRHN-UHFFFAOYSA-N'
    #print('Enter number of similar structures desired: ')
    n = input('Specify the Amount of Records you Would Like to Retrieve From PubChem:\n')
    print(' It seems the time has come for the boy without a fairy to begin his journey..')
    status = 1
    analogous = []
    try:
        inhibitor_info = pcp.get_compounds(inhibitor, 'inchikey', as_dataframe=True)
        #pcp.get_compounds(identifier, type of identifier, creates an object as a pandas dataframe (True))
        inhibitor_cid = inhibitor_info.index[0].astype('str') 
        print('Inhibitor is :\n', inhibitor_info)
    except:
        print('Unable to find structure')
        status = 0
    try:
        print('Finding similar structures...')
        similar = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='similarity', listkey_count=n)
        print('Similair Structure is :', similar)
    except:
        print('Unable to find similar structures')
        status = 0
    try:
        print('Finding substructures...')
        substructure = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='substructure', listkey_count=n)
        print('Substructure is :', substructure)
    except:
        print('Unable to find substructures')
        status = 0
    try:
        print('Finding superstructures...')
        superstructure = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='superstructure', listkey_count=n)
        print('Superstructure is :', superstructure)
    except:
        print('Unable to find superstructure')
        status = 0
    if status == 1:
        analogs = similar + substructure + superstructure
        print('analogs are :\n', analogs)
        inchikeys = []
        for compound in analogs:
            inchikeys.append(str(compound.inchikey))
        analogous = pd.DataFrame({'Similar_Structure InchiKeys': inchikeys})
        analogous.drop_duplicates()
        analogous.reset_index(drop=True)
        analogous.to_csv('similar_compounds.txt')
    return analogous, status


[analogous, status] = similarity_search(path, all_rxns_doc)