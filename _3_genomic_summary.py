# Creates summary matrix of all complete genomes and their EC numbers
# -*- coding: utf-8 -*-
import os;
import re;
import numpy as np

# This function creates the EC binary summary matrix, by going through all of the DIAMOND search outputs and denoting which
# EC numbers are present in each genome, by using a 1 or 0 for EC number status
# This function requires the location of the DIAMOND (Buchfink et al., 2021) search results found in diamond_impl, name of the domain
# Input requires the list of EC numbers, DIAMOND search results, and domain name
# Output is a space separated textfile that should be num genomes x num of EC num as well as the location of the file
def genome_extractor(diamond_folder, name):
    # Changes the directory to the location of the DIAMOND search outputs
    os.chdir(diamond_folder)
    print(os.getcwd())
    # Opens the list of of EC numbers
    ec_open = np.loadtxt('/projects/jodo9280/EcoDr/EcoDr/EC_library.csv',
                         dtype='str')
    big_matrix = ["Name_of_Genome"]
    # Asks user to input name for EC matrix
    # input_name = input("Save EC binary summary matrix as (no spaces or capital letters): ")
    # Specifies document to be a csv type
    # file_name= input_name+".csv"
    # file_name = "synbio1_big_matrix.csv"
    if name == "":
        file_name = os.path.abspath(diamond_folder).rsplit('/', 9)[4] + '_binary_matrix.txt'
        print(os.path.abspath(diamond_folder).rsplit('/', 9))
        print(file_name)
    else:
        file_name = name
    new_dir = diamond_folder + '/' + file_name
    # Checks to see if the document already exists using full pathway name
    if os.path.exists(new_dir):
        pass
        #print("Summary Matrix exists")
        #return [new_dir, file_name]
    else:
        for ec_force in ec_open:
            # Creates a horizontal header of all of the EC names
            big_matrix.append(ec_force)
        # Goes through all of the DIAMOND outputs in the folder
        # Goes through all of the output files, each one is opened and read one line at a time. The lines are split to
        # extract the EC numbers found in each line. If the EC number found in the DIAMOND output matches an
        # EC entry in the list, the status is changed from a zero to a one. The binary status is catalogued horizontally
        # for each genome, and following genomes are vertically stacked
        for item in os.listdir(diamond_folder):
            if item.endswith("_matches.tsv"):
                print(item)
                # Finds the name of the DIAMOND output file
                genome = [item] #Turns the GCF's into a list, where the GCF names in the matrix come from. 
                genome_runner_ec = [item] #Turns the GCF's into a list, where the EC is appended
                print(genome)
                # Iterates through all of the EC numbers (1:8197)
                
                GCF = open(item, 'r') # CBM Added
                
                for line in GCF: # CBM Added
                    print(line)
                    no_tab = line.split('\t')
                    first_ec = no_tab[1].split("?")
                    separate_ec = first_ec[1].split(";_")
                    genome_runner_ec.append(separate_ec)

                for ec in ec_open:
                    # print("EC we actually are looking for "+ ec)
                    # Opens individual DIAMOND output files
                    #CBM GCF = open(item, 'r')
                    # Sets default for EC status is zero, meaning absent
                    #CBM ec_now = 0
                    # Takes the first line in the DIAMOND output file and splits it based on tab separation
                    # Takes the second column of the split line, which has EC numbers separated by a ?, ;_
                    # Strings splits have a new name assigned to them
                    #CBM for line in GCF:
                    #CBM    print(line)
                    #CBM    no_tab = line.split('\t')
                    #CBM    first_ec = no_tab[1].split("?")
                    #CBM    separate_ec = first_ec[1].split(";_")
                    #CBM    print("Seperate EC Likely Nightmare "+ separate_ec[0])
                        # Checks for a full match between the EC number listed in the DIAMOND output and the EC number
                        # found in the separate document
                    #CBM    if re.fullmatch(ec, first_ec[1]) is not None:  # looks for full match of first EC number
                    #CBM        ec_now = 1
                        # In the case that there are more than one EC separated by ;, the function iterates through the list
                        # and sees if there is a full match between the listed EC and the list
                    #CBM    for i in separate_ec:
                    #CBM        if re.fullmatch(ec, i) is not None:  # looks for full match of any other ECs listed
                    #CBM            ec_now = 1
                    ec_now = 0
                    if ec in genome_runner_ec:
                        ec_now = 1

                    # 1 or 0 will be appended to the summary matrix for each EC value in the list
                    genome.append(ec_now)
                    #print(genome)
                # Vertical stacking occurs for each genome in the DIAMOND output folder
                big_matrix = np.vstack([big_matrix, genome])
        #print(big_matrix)
        # Saves matrix as a text file for further analysis
        np.savetxt(file_name, big_matrix, fmt='%s')
        # Returns the location of the summary matrix and the name of the file
        print(new_dir)
        return [new_dir, file_name]
##=============================================Citations==============================================================##
#Buchfink B, Reuter K, Drost HG, "Sensitive protein alignments at tree-of-life scale using DIAMOND", Nature Methods 18, 366–368 (2021). doi:10.1038/s41592-021-01101-x
genome_extractor('/projects/jodo9280/EcoDr/EcoDr/fungi_2024_01_16_Assembly Summary File/fungi_2024_01_16_Assembly Summary File_FASTA_&_DIAMOND', '')
#perhaps look at a binary search

