import streamlit as st
import numpy as np
import pandas as pd
import os
import shutil
import os.path
import numpy as np 
import pandas as pd 
import numpy as np 
red = "\033[91m"
reset_color = "\033[0m"
import seaborn as sns
import matplotlib.pyplot as plt
import tempfile
from EnCen_Functions import EC_extract, tsv_to_fasta, diamond_impl, genome_extractor_ref, genome_extractor_syn, genome_to_genome_diffcomp, read_in_binary_matrix, calculating_distance, pass_to_distance, upload_file, upload_file2, move_files_to_folder
import altair as alt
from streamlit.runtime.scriptrunner import add_script_run_ctx,get_script_run_ctx
from subprocess import Popen
import warnings
warnings.filterwarnings("ignore")
#_______________________________________________________________________________________

st.markdown("<h1 style='text-align: center;'>EcoGenoRisk</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 25px; '>Metagenomic Synthetic Biology Threat Assessment</h1>", unsafe_allow_html=True)

# st.markdown('### Metagenomic Synthetic Biology Risk Assessment')
st.divider()
with st.expander("### Instructions"):
    st.write(':blue[Developed by John Docter (john.docter@colorado.edu), University of Colorado - Boulder]')
    st.write('This is a simple interface for the EcoGenoRisk data pipeline.')
    st.write('User is required to have the amino acid files of the synthetic organism as well as the amino acid files of the organism in the environment they are checking against')
    st.write('Simply follow the prombts and the program will do the rest')
    st.write('Streamlit, the package used to create this GUI, has limits in terms of file size and upload. For larger analyses, please refer to EcoGenoRisk Source Code on Github')

#Ask for home directory and where all the files should be saved______________________________________________________________________________________________________________
home_dir = st.text_input('Please Enter the filepath where you would like all outputs saved')
#/home/anna/Documents/EcoGenoRisk_Paper_Revisions/GUI_Output
if not home_dir:
     st.stop()
else:  
    st.write('All outputs will be saved to ' + home_dir)
st.divider()



#Create Unitprot & EC_Library________________________________________________________________________________________
if os.path.isfile(home_dir +'/EC_library.csv'):
        st.write(":green[EC Library Detected]")
else:
    with st.spinner('Creating EC_Library'):
        EC_extract()
    st.success('EC_Library Created')
    st.write(home_dir)

if os.path.isfile(home_dir + '/uniprot.fasta'):
     st.write(':green[Protein Library Detected]')
else: 
    with st.spinner('Creating Protein Reference Library'):
        tsv_to_fasta()
    st.success('Protein Reference Created')


#Upload Synbio .faa file____________________________________________________________________________
st.header('Synbio File Upload')
uploaded_file = st.file_uploader("Please upload the synbio .faa file you would like to analyze", type='.faa', key = 'IW_syn')
if not uploaded_file: 
    st.stop()
if uploaded_file:
    dest_path = os.path.join(home_dir, uploaded_file.name)
    with open(dest_path, 'wb') as f:
        f.write(uploaded_file.getvalue()) #uploaded file is in the home dir at this point 


# #Synbio Diamond Processing and outputs synbio functional profile__________________________________________________________________________
# #Saves to home directory 

reference = (home_dir + '/uniprot.fasta')
name = uploaded_file.name
with st.spinner('Diamond Aligner Matching Synbio.faa Sequences to Unitpro Reference'):
    diamond_syn = diamond_impl(home_dir, name, reference) #returns the output folder, in this case home_dir



#Genome Extractor_______________________________________________________________________________________________
output2 = genome_extractor_syn(diamond_syn, name, home_dir)
st.success('Synbio Functional Profile Created')


# for item in os.listdir(path):
#     if item.endswith('_profile'):
#         source = os.path.join(synbio, item)
#         destination = os.path.join(functional_folder, item)
#         shutil.move(source, destination)






#Upload Pre-Made Metagenome Functional Profile_________________________________________________________
# with st.expander('## Metagenome Name and Upload'):
#     name = st.text_input('Metagenome', '')
#     st.write('You entered', name)
#     uploaded_file = st.file_uploader("Please upload the Biome binary matrix you would like to analyze against", type='.faa', accept_multiple_files=True, key='IW')
#     if not uploaded_file:
#         st.stop()
#     if uploaded_file:
#         for f in uploaded_file:
#             IW = '/Users/johndocter/Documents/Test Directory for Streamlit '
#             temp_dir = tempfile.mkdtemp()
#             path = os.path.join(temp_dir, f.name)
#             with open(path, "wb") as file:
#                     file.write(f.getvalue())
#             shutil.move(path, IW) #Takes the file and moves it into the temporary directory 
#             shutil.rmtree(temp_dir)
#     else:
#         st.write('Waiting on File Upload')

#Pause and ask for another metagenome
intake = st.selectbox('Would you like to continue the analysis?', ['Yes', 'No', 'Only a sith deals in absolutes'])
if intake == 'Yes':
    st.write('continue')
if intake == 'No':
    st.write('stop')





#Difference Scoring against all uploaded metagenomes_____________________________________________________________________________
#Saves to home directory 







#Visualization____________________________________________________________________________________


