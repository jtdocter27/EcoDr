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
    os.chdir(path)
    #print('Enter your inhibitors InChI-Key code: ')
    inhibitor = 'LRHPLDYGYMQRHN-UHFFFAOYSA-N'
    #print('Enter number of similar structures desired: ')
    n = input()
    status = 1
    analogous = []
    try:
        inhibitor_info = pcp.get_compounds(inhibitor, 'inchikey', as_dataframe=True) #retrieves the compound from PubChem's Database
        inhibitor_cid = inhibitor_info.index[0].astype('str') 
    except:
        print('Unable to find structure')
        status = 0
    try:
        print('Finding similar structures...')
        similar = pcp.get_compounds(inhibitor_cid, 'cid', searchtype='similarity', listkey_count=n)
        print('Similair is :', similar)
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
        inchikeys = []
        for compound in analogs:
            inchikeys.append(str(compound.inchikey))
        analogous = pd.DataFrame({'Similar_Structure': inchikeys})
        analogous.drop_duplicates()
        analogous.reset_index(drop=True)
        analogous.to_csv('similar_compounds.txt')
    return analogous, status

[analogous, status] = similarity_search(path, all_rxns_doc)