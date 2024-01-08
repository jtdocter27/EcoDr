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
##_______________________________________________________________###
##File_Creation##
reference_library = 'uniprot.fasta'
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

