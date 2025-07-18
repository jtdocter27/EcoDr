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
from EnCen_Functions import diff_score, EC_extract, tsv_to_fasta, diamond_impl, genome_extractor_syn,  EC_corrector
import altair as alt
from streamlit.runtime.scriptrunner import add_script_run_ctx,get_script_run_ctx
from subprocess import Popen
import warnings
warnings.filterwarnings("ignore")
from matplotlib.colors import Normalize
#_______________________________________________________________________________________

st.markdown("<h1 style='text-align: center;'>EcoGenoRisk</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 25px; '>Metagenomic Synthetic Biology Threat Assessment</h1>", unsafe_allow_html=True)
# st.markdown("<h1 style='text-align: center; font-size: 25px; '>Developed by John Docter (john.docter@colorado.edu), University of Colorado - Boulder>", unsafe_allow_html=True)

# st.markdown('### Metagenomic Synthetic Biology Risk Assessment')
st.divider()
st.header('Instructions')
with st.expander("### Start Here"):
    st.write('This is a simple interface for the EcoGenoRisk pipeline. Follow the prombts and the program will output a threat assessment')
    st.write('User is required to have the amino acid (.faa) files of the synthetic organism, or any .faa file of comparison organism. Test Files are available in the associated library for metagenome comparison')
    st.write('For larger analyses, please refer to EcoGenoRisk Source Code on Github: :blue[https://github.com/UCBoulder/EcoGenoRisk]')
#Ask for home directory and where all the files should be saved______________________________________________________________________________________________________________
    home_dir = st.text_input('Please Enter the filepath where you would like all outputs saved')
    # home_dir = '/home/anna/Documents/EcoGenoRisk_Paper_Revisions/GUI_Output'
    if not home_dir:
        st.stop()
    else:  
        st.write(':green[All outputs will be saved to ]  ')
        st.write(home_dir)



#Create Unitprot & EC_Library________________________________________________________________________________________
st.header('Enzyme and Protein Library Creation')
with st.expander('Create Reference Libraries'):
    if st.button('Press to create Expasy and Unitprot Libraries'):
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
    # else:
    #     st.stop()
    # else:
    #     st.stop()

#Upload Synbio .faa file____________________________________________________________________________
st.header('Synbio File Upload')
with st.expander('Upload'):
    uploaded_file_synbio = st.file_uploader("Please upload the synbio .faa file you would like to analyze", key = 'IW_syn')
    if not uploaded_file_synbio: 
        st.stop()
    if uploaded_file_synbio:
        synbio_path = os.path.join(home_dir, uploaded_file_synbio.name)
        with open(synbio_path, 'wb') as f:
            f.write(uploaded_file_synbio.getvalue()) #uploaded file is in the home dir at this point 
    #Parsing to align with metagenomes______________________________________________________________________



    # #Synbio Diamond Processing and outputs synbio functional profile__________________________________________________________________________

    reference = (home_dir + '/uniprot.fasta')
    file_name = uploaded_file_synbio.name
    with st.spinner('Diamond Aligner Matching Synbio.faa Sequences to Unitprot Reference'):
        diamond_syn = diamond_impl(home_dir, file_name, reference) #returns the output folder, in this case home_dir




#Genome Extractor_______________________________________________________________________________________________
    output2 = genome_extractor_syn(diamond_syn, file_name, home_dir)
    st.success('Synbio Functional Profile Created')

    #Parsing to align with metagenomes______________________________________________________________________
    with st.spinner('Parsing Enzymes'):
            EC_corrector(home_dir)


#Upload Pre-Made Metagenome Functional Profile and save to home directory_________________________________________________________
st.header('Metagenome Upload')
with st.expander('## Please choose from any of the pre-processed metagenomes. Multiples are ok'):
    
    file_found = True
    for all_files in os.listdir(home_dir):
        if 'Score' in all_files:
            st.write(':green[Scores Detected]')
            file_found = False
            break

    if file_found:
        uploaded_file_meta = st.file_uploader(" ", accept_multiple_files= True, key='IW')
        if not uploaded_file_meta:
            st.write('Waiting on File Upload')
            st.stop()

        if uploaded_file_meta:
            for every_file in uploaded_file_meta: 
                biome_path = os.path.join(home_dir, every_file.name)
                new_name = every_file.name + ' Difference Score'
                synbio_func_path = home_dir +'/' + 'BioPesticide Parsed.txt'
                with open(biome_path, 'wb') as f:
                    f.write(every_file.getvalue())
                with st.spinner('Working...'):
                    diff_score(synbio_func_path, biome_path)
                with open('Absolute_Difference_Comparison_Score.txt', 'r') as f:
                    file_content = f.read()
                os.rename('Absolute_Difference_Comparison_Score.txt', new_name )
    

    


#3) Then, header with Visualization for score. We'll just hide the fact that scores are being calculated in the upload. 
st.header('Scoring', divider='grey')
if st.button('Press to See Threat Assessment', key='IW_3'):
    top_ten_master_list = []
    for file in os.listdir(home_dir):
        if 'Score' in file:
            biome_name = "_".join(file.split("_")[:2])
            biome_name = biome_name.replace('_', " ")
            score_df = pd.read_csv(home_dir + '/' + file, sep='\t')
            score_df = score_df.drop(score_df.columns[[0]], axis = 1)
            top_ten = score_df[:10]
            top_ten["Organisms Compared to Synbio"] = top_ten["Organisms Compared to Synbio"].str.replace("_matches.tsv", "", regex=False)
            top_ten = top_ten.rename(columns={'Organisms Compared to Synbio': 'Organism Bin ID'})
            top_ten_master_list.append(top_ten)
            # print(top_ten)
            # final_hist = pd.concat(top_ten_master_list, axis=1, ignore_index=True)
            # st.dataframe(final_hist)
            st.subheader(biome_name)
            fig, ax = plt.subplots()
            norm = Normalize(vmin=top_ten["Difference Score"].min(), vmax=top_ten["Difference Score"].max())
            cmap = plt.cm.Greys_r  # reversed Greys: darker = lower

            # Map each value to a color
            colors = [cmap(norm(val)) for val in top_ten["Difference Score"]]
            ax = sns.barplot(data=top_ten, x = 'Organism Bin ID', y = 'Difference Score', ax=ax, palette='magma')
            ax.bar_label(ax.containers[0], fontsize=10);
            plt.xticks(rotation=75)  

            plt.tight_layout()  
            plt.show()
            st.pyplot(fig)



            # st.success('Read correct number of files')    
        # else:
            # st.write('Error in threat assessment')
    
    # final_hist = pd.concat(top_ten_master_list, axis=1, ignore_index=True)
    # st.dataframe(final_hist)
    # fig, ax = plt.subplots()
    # sns.histplot(data=final_hist, x = ), ax=ax)
    # st.pyplot(fig)







# %%
