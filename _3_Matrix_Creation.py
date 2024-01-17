import os;
import re;
import numpy as np

def matrix_creation(diamond_folder, name):
    #this chunk is just making sure the EC's append to our final matrix
    os.chdir(diamond_folder) 
    ec_open = np.loadtxt('/projects/jodo9280/EcoDr/EcoDr/EC_library.csv',
                         dtype='str')
    matrix = []
    if name =='':
        file_name = 'Binary_Matrix.txt'
        new_dir = diamond_folder + '/' + file_name
    for ec in ec_open:
        matrix.append(ec)
    ##____________________________________________________________________________________##
    #this chunk makes a list of all the GCF_matches names
    for item in os.listdir(diamond_folder): #lists the names of all files in diamond_folder
        if item.endswith('_matches.tsv'):
            print(item)
            GCF_matches = [item]
    
    for ec in ec_open:
        GCF_matches = open(GCF_matches, 'w+')
        ec_no = 0
        for line in GCF_matches:
            split1 = line.split('\t') #splits each line in GCF by tabs and puts each item into the variable
            print(split1)
            first_ec = split1[1].split('?') #splits the 
            print(first_ec)
            second_ec = first_ec[1].split(';_')
            print(second_ec)

matrix_creation('/projects/jodo9280/EcoDr/EcoDr/archaea_2024_01_16_Assembly Summary File/archaea_2024_01_16_Assembly Summary File_FASTA_&_DIAMOND', '')

