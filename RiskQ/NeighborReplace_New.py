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
biome = pd.read_csv('/home/anna/Desktop/JD_Niche_OverLap (Git)/Niche_JD/Eco_V2/RiskQ/biome_data.tsv', sep='\t')
lineage = biome['Bin Lineage'] #We want just the genus and species as that is the BLAST output 
genusspecies = biome['Bin Lineage'].str.rsplit(';', n=2).str[-2:].str.join('')
genusspecies = genusspecies.reset_index(drop=True)
genusspecies = genusspecies.to_frame()
print(genusspecies)



##3) BLASTn 
sequence1=final[0]
result_stream = Blast.qblast('blastn', 'refseq_rna', sequence1)
print('Blasting.....')

with open("blast_output.xml", "wb") as out_stream: #writes the contents to a file and then reopens to so if there's an issue, don't have to rerun BLAST all over again
    out_stream.write(result_stream.read())
result_stream.close()




#4) Parse Blast Output for relevant information 
result_stream = open("blast_output.xml", "rb")
blast_record = Blast.read(result_stream)
# print(len(blast_record))

all_records = len(blast_record)
all_blast_species = []
for i in range(all_records):
    hit = blast_record[i]
    text = hit.target.description
    # print(text.split())
    text= text.split()[:2]
    text = ' '.join(text)
    all_blast_species.append(text)

    # all_blast_species.append(hit.target.description)

print(all_blast_species) #we now have all the species that come up on BLAST



#5) Merge on scientific name and write results to an external file. 
#Turn all blast species into dataframe 
all_blast_species_df = pd.DataFrame(all_blast_species)
print(all_blast_species_df.shape)
remaining = pd.merge(genusspecies, all_blast_species_df,  how='right')

