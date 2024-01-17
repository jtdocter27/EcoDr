import os;
import re;
import numpy as np

def matrix_creation(diamond_folder, name):
    os.chdir(diamond_folder)
    ec_open = np.loadtxt('/projects/jodo9280/EcoDr/EcoDr/EC_library.csv',
                         dtype='str')
    matrix = []
    if name =='':
        file_name = 'binary_matrix.txt'
    for ec in ec_open:
        matrix.append(ec)
    print(matrix) 

matrix_creation('/projects/jodo9280/EcoDr/EcoDr/archaea_2024_01_16_Assembly Summary File/archaea_2024_01_16_Assembly Summary File_FASTA_&_DIAMOND', '')

