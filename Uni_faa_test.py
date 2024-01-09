#####-----------------------------------------------------------###
#This script is for testing automating the Uniprot download and fasta creation workflow
#FASTA
#Will then be plugged into _2_ line 200 
####------------------------------------------------------------###
import requests
import time
from fake_useragent import UserAgent
import csv
import os
import pandas as pd
##_______________________________________________________________###
##File_Creation##
reference_library = '/Users/johndocter/Documents/EcoDr/uniprot.fasta' 
ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}
uniport_url = 'https://rest.uniprot.org/uniprotkb/stream?fields=accession%2Cec%2Csequence&format=tsv&query=%28%28ec%3A*%29%29+AND+%28reviewed%3Atrue%29'
time.sleep(4)
uniprot = requests.get(uniport_url, headers=header)
print('uniport library imported')
if uniprot.status_code == 200:
    with open(reference_library, 'w+') as reference_library:
            # Copies content from the website, pastes it into assembly_summary file
            #open the blacn assembly summary.txt file in writing mode as 
        reference_library.write(uniprot.text)
        # Closes out document
        #The original code is: shutil.move(os.getcwd() + '/' + text_file, folder1_name)
#original_path = os.path.join(os.getcwd(), text_file)
#shutil.move(original_path, text_file)
print('Uniprot Reference File Has Been Created')

##________________________________________________________________________###
##File Editing##
uni_path = os.path.abspath('uniprot.fasta')
with open(uni_path, 'r', newline ='') as final_fasta:
    tsv_reader = csv.reader(final_fasta, delimiter ='\t')
    tsv_data = [row for row in tsv_reader]

remove_top_row = tsv_data[1:]
carrot_fasta = [['>' + row[0]] +row[1:] for row in remove_top_row]


with open(uni_path, 'w+', newline='') as final_fasta:
    tsv_writer = csv.writer(final_fasta, delimiter='\t')
    tsv_writer.writerows(carrot_fasta)

##File Editing 2 Pandas Attempt
#fasta_df = pd.read_csv(uni_path, delimiter='\t')
#new_row = fasta_df.iloc[:, 2].shift(-1).dropna().reset_index(drop=True)
#fasta_df = pd.concat([fasta_df, new_row], axis = 0, ignore_index=True)

#fasta_df.to_csv('uniprot.fasta', sep='\t', index =False)

#File Editing 3 Direct
# Assuming you have a TSV file named 'input_file.tsv'

with open(uni_path, 'r') as fasta_editted:
    lines = fasta_editted.readlines()

for index, line in enumerate(lines):
    # Split the line into columns based on '\t'
    columns = line.strip().split('\t')

    # Check if the line has at least three elements
    if len(columns) >= 3:
        # Create a new line by adding a newline character after the third element
        new_line = '\t'.join(columns[:2]) + '\t' + columns[2] + '\n'

        # Insert the new line beneath the original line
        lines.insert(index + 1, new_line)

# Write the modified content back to the file
with open(uni_path, 'w') as final: 
    final.writelines(lines)
