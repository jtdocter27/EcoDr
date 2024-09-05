###September 5th, 2024
##This script is a taxnomic similairty search between the input synbio organism and all of the organisms present in the biome 
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO






#________________________________________________________________________________________________________________________________________________________________________________
##1) Input Synbio FASTA
final = []
sixteen_s = SeqIO.parse('/home/anna/Downloads/16S.fasta', 'fasta')
for NA in sixteen_s:
     sequence = str(NA.seq)
     final.append(sequence)
print(final) #This is a list of all the sequences 

##2) Input Biome FASTA


##3) BLASTn 


##4) Parse Bin Lineage and merge 


#4) Output most suscetible biome 