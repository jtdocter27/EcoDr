###September 5th, 2024
##This script is a taxnomic similairty search between the input synbio organism and all of the organisms present in the biome 
#This script utilizes the new blast on biopython. https://biopython.org/docs/latest/Tutorial/chapter_blast.html
import Bio
from Bio import Blast
from Bio import SeqIO
import pandas as pd 

Blast.email = 'john.docter@colorado.edu'
#________________________________________________________________________________________________________________________________________________________________________________
##1) Input Synbio FASTA
final = []
sixteen_s = SeqIO.parse('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/RiskQ/Vibrio_Natriegens_16S.fasta', 'fasta')
for NA in sixteen_s:
     sequence = str(NA.seq)
     final.append(sequence)
# print(final[0]) #This is a list of all the sequences 


#2) Import Biome FASTA and parse for genus and species 



##3) BLASTn 
sequence1=final[0]
result_stream = Blast.qblast('blastn', 'refseq_rna', sequence1)
print('Blasting.....')

with open("blast_output.xml", "wb") as out_stream: #writes the contents to a file and then reopens to so if there's an issue, don't have to rerun BLAST all over again

    out_stream.write(result_stream.read())
result_stream.close()
result_stream = open("blast_output.xml", "rb")


#4) Parse Blast Output for relevant information 
blast_records = Blast.parse(result_stream)
print(blast_records)


#5) Merge on scientific name and write results to an external file. 




