# -*- coding: utf-8 -*-
#Initial Imports
import gzip#; print('gzip version: ', gzip.__version__)
import os#; print('os version: ', os.__version__)
import re#; print('re version: ', re.__version__)
import shutil#; print('shutil version: ', shutil.__version__)
import requests#; print('requests version: ', requests.__version__)
import wget#; print('wget version: ', wget.__version__)
import subprocess#; print('subprocess version: ', subprocess.__version__)
import time#; print('time version: ', time.__version__)
from datetime import datetime
from subprocess import PIPE, Popen
from fake_useragent import UserAgent
import os.path
from os import path
from Bio.ExPASy import Enzyme
import csv


##===================================================================================================================##
#tsv_to_fasta takes in a tsv file generated from Uniprot and converts it into a FASTA format for use by DIAMOND
##Refernce_library is where the file is saved to. Output is the same. 
###This initial step just downloads the TSV, reads it in, and writes it to the file name specified in reference_library
def tsv_to_fasta():
    reference_library = 'uniprot.tsv' 
    #this creates a file named 'uniprot.tsv' on the working directory. Should show within the EcoDr/EcoDr folder. 
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    uniprot_url = 'https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cec%2Csequence&format=tsv&query=%28%28ec%3A*%29%29+AND+%28reviewed%3Atrue%29'
    time.sleep(4)
    uniprot = requests.get(uniprot_url, headers=header)
    if uniprot.status_code == 200:
        with open(reference_library, 'w+') as reference_library:
            reference_library.write(uniprot.text)
    print('Uniprot Reference File Has Been Created')
####this step takes it the initial tsv and converts it to FASTA
    input = os.path.abspath('uniprot.tsv')
    output = 'uniprot.fasta'
    with open(input, 'r') as input_file, open(output, 'w') as output_file:
        header=next(input_file)
        for line in input_file:
            carrot = f'>{line}'
            new_row = re.sub(r'(.*?\t.*?)\t', r'\1\n', carrot, 1)
            new_row_with_tab_replaced_by_question_mark = new_row.replace("\t", "?")
            # Be careful with the symbols used for replacement, as they have to align with the genomic summary string parsing
            output_row_with_space_replaced_with_ampersand = new_row_with_tab_replaced_by_question_mark.replace("; ", ";_")
            #new_row2 = re.sub(r'(.*?\t.*?)\t', r'$', new_row, 0)
            #this is regex, for the record. 
            output_file.write(output_row_with_space_replaced_with_ampersand)
    print('FASTA has been created from TSV and is named', output)
##===================================================================================================================##
###This function extracts the EC numbers from Expasy https://www.expasy.org/resources/enzyme
def EC_extract():
    ec_library = 'EC_library.csv' 
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    ec_url = 'https://ftp.expasy.org/databases/enzyme/enzyme.dat'
    time.sleep(4)
    ec = requests.get(ec_url, headers=header)
    if ec.status_code == 200:
        with open(ec_library, 'w+') as ec_file:
            ec_file.write(ec.text)
    print('EC List Has Been Created')
###This step creates the list 
    handle = open(ec_library)
    records = Enzyme.parse(handle)
    ecnumbers = [record["ID"] for record in records]
    #print(type(ecnumbers)) #This is a list at this point in the code
    path = os.path.abspath(ec_library)
    with open(path, 'w+', newline='') as csv_file:
        csv_file = csv.writer(csv_file)
        for item in ecnumbers:
            csv_file.writerow([item])
    print('EC list Has Been Created')
##===================================================================================================================##
# Asks for input for domain, returns a specific NCBI RefSeq URL for protein file download
# Stores the name of domain for future naming convention
# This has been checked for each domain
def input_domain():
    # Creates a timestamp in form of date,month,year for naming convention
    now = datetime.now()
    str_date = now.strftime("%Y_%m_%d") # _%H-%M-%S")
    # domain = input("Enter domain:")
    # Change when done testing
    domain = input("Enter archaea, bacteria, or fungi: ")
    folder1_name = domain + "_" + str_date + "_" + 'Assembly Summary File'
    # Changes path to this new location to store all of the files in
    # Creates a new folder in this path. Folder name will start with the timestamp and end with the domain name
    # All new files/folders will be created in this folder
    if os.path.exists(os.getcwd() + "/" + folder1_name):
        print(folder1_name + " already exists on this directory")
    else:
        os.makedirs(folder1_name)
    os.chdir(folder1_name)
    # Converts all domain input for consistency
    lower_case = domain.lower()
    print('You entered', lower_case)
    ncbi_url = ''
    # Finds corresponding domain name, returns NCBI RefSeq ftp domain name for protein file download
    if lower_case == 'archaea':
        ncbi_url = 'https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt'
        print("Archaea url selected")
    elif lower_case == 'bacteria':
        ncbi_url = 'https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt'
        print("Bacteria url selected")
    elif lower_case == 'fungi':
        ncbi_url = 'https://ftp.ncbi.nlm.nih.gov/genomes/refseq/fungi/assembly_summary.txt'
        print("Fungi url selected")
    else:
        print("Invalid Input. Check your spelling and spaces!")
    print("All new files will be saved in: ", folder1_name)
    # Returns the new folder name (time stamp+ domain name) and the ncbi url
    return [ncbi_url, folder1_name]


##===================================================================================================================##
#Takes in a string, the ncbi URL, and the folder name defined in the previous function
#Retrieves the Assembly Summary from NCBI and puts it into the name of the folder defined above
def checking_assembly_file(text_file, ncbi_url,
                           folder1_name):
    #print(os.getcwd())
    # Allows retriving and parsing for a web browser, header changes permissions
    # Examples of user agent function for web scraping: https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit-a-k-a-and-generate-user-agent
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    # Checks if file exists already to not spam NCBI
    #print(os.getcwd() + '/' + text_file)
    if os.path.exists(os.getcwd() + '/' + text_file):
        print("Assembly Summary File Already Exists and Has Been Located")
        #return "Assembly Summary File Already Exists"
    else:
        # Pauses run for 4 seconds to avoid spam
        time.sleep(4)
        # Permissions for opening file through NCBI
        temp_genome_list = requests.get(ncbi_url, headers=header)
        print('Assembly File Has Been Found on NCBI Website')
        if temp_genome_list.status_code == 200:
            with open(text_file, 'w+') as genome_list_out:
            # Copies content from the website, pastes it into assembly_summary file
            #open the blacn assembly summary.txt file in writing mode as 
                genome_list_out.write(temp_genome_list.text)
        # Closes out document
        #The original code is: shutil.move(os.getcwd() + '/' + text_file, folder1_name)
        original_path = os.path.join(os.getcwd(), text_file)
        shutil.move(original_path, text_file)
        print('Assembly File Has Been Created and Moved to', folder1_name)
    print('Checking Assembly File Success')

##===================================================================================================================##
# Creates a protein file folder for the most recent inquiry
# Looping through assembly summary file, finding the samples that have a complete genome, and downloading the FTP # Inputs requires the filled out assembly summary text file (derived from checking_assembly_file) and domain name (derived from input_domain)
# Outputs the location of the FASTA protein files for all complete genome organisms

#text_file is the assembly summary, folder1 is just the domain and the date the code was run
def file_extraction(text_file, folder1_name):
    # Prints current directory
    print('The Current Directory is', os.getcwd())
    # Checks to see if a protein file specific folder already exist for the most recent domain inquiry
    # Prints a statement if the folder is already present and the protein files are extracted
    if os.path.exists(os.getcwd() + "/" + folder1_name + "_FASTA_&_DIAMOND"):
        print('Protein Files are Already Extracted')
        destination = (os.getcwd() + "/" + folder1_name + "_FASTA_&_DIAMOND")
    else:
        # If folder is not present, creates a protein file specific folder and saves the pathway of folder as the
        # Desired destination for protein files
        os.makedirs(folder1_name + "_FASTA_&_DIAMOND")
        # Changes current directory so any folder created from here on will be nested inside this one
        destination = os.path.abspath(folder1_name + '_FASTA_&_DIAMOND')  # creates a domain specified folder pathway
        with open(text_file, 'r') as assembly_summary:
            # Reads one line at a time, iterating through the doc
            assembly_summary.readline()
            for line in assembly_summary:
                # Splits line by tab to reference a specific column in the document
                output = line.split("\t")
                # References specific column for assembly level, if status is complete, then extracts the ftp path
                if re.match(output[11], "Complete Genome"):
                    # Extracting the ftp path link, this website takes you to index of all genomes that are available for download
                    link = output[19]
                    org_name = link
                    # Species name is found by extracting the genome accession number/ASM name that is on the right side of the backslash
                    species_name = re.search(r'(.*)/(.*)', org_name).group(2)
                    # Download url is constructed by using the website archetype for NCBI directories
                    # Data is organized by using a series of directories named as the species binomial
                    # For more information: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/002/287/175/GCF_002287175.1_ASM228717v1/README.txt
                    # If FASTA genomic sequences are desired instead, then change _protein.faa.gz to genomic.fna.gz
                    url_new = link + '/' + species_name + '_protein.faa.gz'
                    # If the protein file for a genome already exists, then print a blank space
                    if os.path.exists(os.getcwd() + "/" + folder1_name + "_protein_file" + "/" + species_name + "_protein.faa"):
                        print("")
                    else:
                        # Downloads faa file using the url constructed above
                        wget.download(url_new)
                        # Creates filename using genome accession number and ASM name
                        download_name = species_name + '_protein.faa.gz'
                        # Finds the location that the file has been downloaded to
                        source = os.path.abspath(download_name)
                        # Moves file into domain specified folder
                        shutil.move(source, destination)
        # Closes opened assembly summary document
        assembly_summary.close()
    # Returns the location of the protein file >>> desired pathway/timestamp_domain/protein_file
    print(destination)
    return destination


##===================================================================================================================##
# Extracting all files and deleting the zip folder
# Input is the location of protein files
# No real output, the function extracts the compressed files
# This code originated from: https://gist.github.com/kstreepy/a9800804c21367d5a8bde692318a18f5
def file_management(destination):
    dir_name = 'x'
    # References those files that are compressed
    extension = ".gz"
    file_name = ''
    os.chdir(destination)
    # Iterates through the protein file folder, destination where the .faa files were downloaded
    for item in os.listdir(destination):
        # Check for ".gz" extension, does not apply to those files that were already extracted
        if item.endswith(extension):
            # Finds full path of files
            gz_name = os.path.abspath(item)
            # Finds file name for file within, GCF and ASM names
            file_name = (os.path.basename(gz_name)).rsplit('.', 1)[0]
            with gzip.open(gz_name, "rb") as f_in, open(file_name, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            os.remove(gz_name)  # delete zipped file

    return 'file management and extraction-- success'
###==================================================================================================================##
# DIAMOND IMPLEMENTATION:
# (1) Creates a diamond-formatted library, completes DIAMOND (Buchfink et al., 2021) search using a curated Uniprot library (reference.dmnd) as well as the
# protein files downloaded for each completely assembled genome.
# (2) Creates a new folder for DIAMOND outputs and moves all outputs into the folder
# Input requires the location of unzipped protein files that was returned in file_extractor as well as the reference document
# Output results in DIAMOND search results, which are lists of EC numbers found cited in each organisms protein sequence
# Function returns the location of the new folder and DIAMOND matches
# -1-new_folder = diamond_impl(destination, '')
# -4-diamond_results_loc = diamond_impl(desired_location)
def diamond_impl(dest, name):
    print(os.getcwd())
    matches = ''
    synbio_specific_folder = dest + "/DIAMOND_matches"
    print("DIAMOND search library is: ", synbio_specific_folder)
    # (1) Creates another folder named DIAMOND matches to store DIAMOND output
    # Note: there might be potential issues with file management and moving to appropriate places! Construct code for folder
    # creation and placement after configuring script compiles without any further issues
    # Checks to see if the folder already exists, and if not creates a new folder
    # Checks to see if the DIAMOND library is present in the new destination
    if os.path.isfile('reference.dmnd'):
        print("Library Detected")
    # If not present, then creates a DIAMOND library by referencing the exact location where the Uniprot library is saved
    # If there currently is no reference library (.dmnd), then command makedb creates a DIAMOND library
    else:
        print("Creation of DIAMOND-formatted library...")
    # To automate the uniprot.fast file rather than hardcoding in the directory, use the following REST API code from Uniprot:
    # https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cec%2Csequence&format=tsv&query=%28%28ec%3A*%29%29+AND+%28reviewed%3Atrue%29
    # Next step, add a ">" symbol at the very beggining of all lines
    # Next step, merge the first two columns by replacing the first \t tab with a $ symbol
    # After, replace the second \t symbol with an end of line \n character
    # This then processes the Uniprot Library into a FASTA file

        makedb = ['diamond', 'makedb', '--in', '/projects/jodo9280/EcoDr/EcoDr/uniprot.fasta', '-d',
                  'Uniprot_Reference_Library.dmnd']  # Reference library full pathway
        #This is a list for the DIAMOND specific makedb function. 
        subprocess.run(makedb)
        #This simply runs the function makedb
        print("Library complete")
    # For item in domain_folder, if item is a faa file, then complete diamond analysis
    for item in os.listdir(dest):
        # Checks for file extension
        if item.endswith('.faa') and not os.path.isfile(
                os.path.basename(os.path.abspath(item)).rsplit('.', 1)[0] + "_matches.tsv"):
            # Finds path of file
            file_path = os.path.abspath(item)
            # Finds the GCF/ASM name of the file by looking at the first part of the name before the .faa notation
            if name == "":
                print(os.path.basename(file_path).rsplit('.',1))
                file_name = (os.path.basename(file_path)).rsplit('.', 1)[0]
            else:
                file_name = name
            # New filename that ends with matches
            matches = file_name + "_matches.tsv"
            print(matches)
            # If genome has not already undergone DIAMOND search and is currently located in the correct folder, then
            # the subprocess function will run the diamond search
            if not os.path.isfile(dest + "/" + matches) and os.path.abspath(matches) != synbio_specific_folder:
                print("Processing ", file_name)
                # DIAMOND search using the full pathway of the protein files, max target sequence outputs only one best
                # match with highest e-value which represent the chance of obtaining a better random match in the same database (Buchfink et al, 2021)
                blastp = ['diamond', 'blastp', '-d', 'Uniprot_Reference_Library.dmnd', '-q', file_path, '-o', matches,
                          '--max-target-seqs', '1', '--outfmt', '6']
                time.sleep(4)
                subprocess.run(blastp)
        # (2) Creates a folder for DIAMOND outputs
        if not os.path.exists(synbio_specific_folder):
            os.makedirs('DIAMOND_matches')
    # Moves all DIAMOND search outputs into the folder
        if item.endswith('_matches.tsv'):
            if os.path.exists(os.path.join(synbio_specific_folder, item)):
                print(f"Overwriting: {item}")
                os.remove(os.path.join(synbio_specific_folder, item))
            shutil.move(os.path.abspath(item), synbio_specific_folder)
    print("diamond_impl--success")
    # Returns the location of the DIAMOND matches folder
    return synbio_specific_folder

##=============================================Citations==============================================================##
# Buchfink B, Reuter K, Drost HG, "Sensitive protein alignments at tree-of-life scale using DIAMOND", Nature Methods 18, 366–368 (2021). doi:10.1038/s41592-021-01101-x
