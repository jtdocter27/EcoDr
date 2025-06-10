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

#_______________________________________________________________________________________

st.markdown("<h1 style='text-align: center;'>EcoGenoRisk</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 25px; '>Metagenomic Synthetic Biology Risk Assessment</h1>", unsafe_allow_html=True)

# st.markdown('### Metagenomic Synthetic Biology Risk Assessment')
st.divider()
with st.expander("### Instructions"):
    st.write(':blue[Developed by John Docter (john.docter@colorado.edu), University of Colorado - Boulder]')
    st.write('This is a simple interface for the EcoGenoRisk data pipeline.')
    st.write('User is required to have the amino acid files of the synthetic organism as well as the amino acid files of the organism in the environment they are checking against')
    st.write('Simply follow the prombts and the program will do the rest')
    st.write('Streamlit, the package used to create this GUI, has limits in terms of file size and upload. For larger analyses, please refer to EcoGenoRisk Source Code on Github')

with st.expander('## Input Name of Metagenome Here'):
    name = st.text_input('Metagenome', '')
    st.write('You entered', name)
    uploaded_file = st.file_uploader("Please upload the Biome .faa file(s) you would like to analyze against", type='.faa', accept_multiple_files=True, key='IW')
    if not uploaded_file:
        st.stop()
    if uploaded_file:
        for f in uploaded_file:
            IW = '/Users/johndocter/Documents/Test Directory for Streamlit '
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, f.name)
            with open(path, "wb") as file:
                    file.write(f.getvalue())
            shutil.move(path, IW) #Takes the file and moves it into the temporary directory 
            shutil.rmtree(temp_dir)
    else:
        st.write('Waiting on File Upload')



#Analysis______________________________________________________________________________________________
# home_dir = '/home/anna/Documents/JGI_soil_genomes' 

# st.header('')
# for mg_to_analyze in choices:
#     if mg_to_analyze == 'industrial wastewater':
#         metagenome_name = 'reference_diamond_analysis_output' #-> folder
#         home_dir = '/home/anna/Documents/JGI_soil_genomes' 
#         # IW = '/home/anna/Documents/JGI_soil_genomes/IW_Metagenome'
#         IW = '/home/anna/Documents/JGI_soil_genomes/' + mg_to_analyze + '_metagenome_bins'
#         # abspath = os.path.abspath()
#     #Automatically Makes a folder for the metagenomic bins to upload into, then asks the user for files and moves those files into the bins folder_____________________________________________________###
#         os.chdir(home_dir)
#         if os.path.exists(IW):
#             shutil.rmtree(IW)
#             os.mkdir(IW)
#         else:
#             os.mkdir(IW)
        


#         #Below is the original file uplaod using tkinter
#         # file_paths = upload_file(home_dir, mg_to_analyze)
#           # upload_location = IW
#         # move_files_to_folder(file_paths, upload_location)
#         st.header(mg_to_analyze.title() + ' Analysis', divider='gray')
#         uploaded_file = st.file_uploader("Please upload the Biome .faa file(s) you would like to analyze against", type='.faa', accept_multiple_files=True, key='IW')
#         if not uploaded_file:
#             st.stop()
#         if uploaded_file:
#            for f in uploaded_file:
#                 temp_dir = tempfile.mkdtemp()
#                 path = os.path.join(temp_dir, f.name)
#                 with open(path, "wb") as file:
#                         file.write(f.getvalue())
#                 shutil.move(path, IW) #Takes the file and moves it into the temporary directory 
#                 shutil.rmtree(temp_dir)
#         else:
#             st.write('Waiting on File Upload')

