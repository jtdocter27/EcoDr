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

from IW_functions import EC_extract, tsv_to_fasta, diamond_impl, genome_extractor, genome_to_genome_diffcomp, read_in_binary_matrix, calculating_distance, pass_to_distance, upload_file, upload_file2, move_files_to_folder

#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a
#Input Block_________________________________________________________________________________________________________________________________________________________________________________________
st.title('Welcome to Environmental Census (EnCen)')
st.write(':blue[A bioinformatics tool for quantifying and displaying synthetic biology risk]')
st.write(':green[Developed by John Docter, Univeristy of Colorado - Boulder]')


intake = st.multiselect('Please choose which available metagenomes you like to analyze', 
                        ['Industrial Wastewater', 'Wastewater Treatment Plant', 'River'])
'You selected: ', intake

choices = [choice.strip().lower() for choice in intake]

#Analysis______________________________________________________________________________________________
home_dir = '/home/anna/Documents/JGI_soil_genomes' 

os.chdir(home_dir)
for file in os.listdir(home_dir):
     if file.endswith(('_output', 'outputs', '_bins', '_profiles')):
        shutil.rmtree(os.path.join(home_dir, file))

for mg_to_analyze in choices:
    if mg_to_analyze == 'industrial wastewater':
        metagenome_name = 'reference_diamond_analysis_output' #-> folder
        home_dir = '/home/anna/Documents/JGI_soil_genomes' 
        # IW = '/home/anna/Documents/JGI_soil_genomes/IW_Metagenome'
        IW = '/home/anna/Documents/JGI_soil_genomes/' + mg_to_analyze + '_metagenome_bins'
        # abspath = os.path.abspath()
    #Automatically Makes a folder for the metagenomic bins to upload into, then asks the user for files and moves those files into the bins folder_____________________________________________________###
        os.chdir(home_dir)
        if os.path.exists(IW):
            shutil.rmtree(IW)
            os.mkdir(IW)
        else:
            os.mkdir(IW)

        # # Example usage
        file_paths = upload_file(home_dir, mg_to_analyze)
        upload_location = IW
        move_files_to_folder(file_paths, upload_location)

    ##__________________________________________________________________________________#Diamond Analysis
        os.chdir(home_dir)
        if os.path.exists(metagenome_name):
            shutil.rmtree(metagenome_name)
            os.mkdir(metagenome_name)
        else:
            os.mkdir(metagenome_name)
        # home_dir = home_dir + "/" + metagenome_name 

        os.chdir(IW)
        diamond = diamond_impl(IW, '') #-> Takes in the path and directory
    # #________________________________________________________________________________# Creating reference functional profile

        dmnd_folder = '/home/anna/Documents/JGI_soil_genomes/reference_diamond_analysis_output'
        ff_name = 'functional_profiles'
        functional_folder = '/home/anna/Documents/JGI_soil_genomes/functional_profiles'
        name = mg_to_analyze + '_metagenome'

        for item in os.listdir(IW):
            if item.endswith(('_matches.tsv', '.dmnd')):
                source = os.path.join(IW, item)
                destination = os.path.join(dmnd_folder, item)
                shutil.move(source, destination)
        

        output = genome_extractor(dmnd_folder, name, home_dir)

        os.chdir(home_dir)
        if os.path.exists(functional_folder):
            shutil.rmtree(functional_folder)
            os.mkdir(ff_name)
        else:#makes a new directory called metagenome_name
            os.mkdir(ff_name)

        for item in os.listdir(dmnd_folder):
            if item.endswith('_profile'):
                source = os.path.join(dmnd_folder, item)
                destination = os.path.join(functional_folder, item)
                shutil.move(source, destination)
            
    #-----------------------------------------------------------------------------------# Organism to analyze matches and functional profile creation 
        synbio = '/home/anna/Documents/JGI_soil_genomes/' + mg_to_analyze + '_synbio_inputs_and_outputs'
        name = 'Synbio'
        syn_folder_name = mg_to_analyze + '_synbio_inputs_and_outputs'
        desired_location2 = '/home/anna/Documents/JGI_soil_genomes'

        os.chdir(home_dir)
        if os.path.exists(synbio):
            print('Synbio directory already exists')
        else:#makes a new directory called metagenome_name
            os.mkdir(syn_folder_name)

       
        
        file_paths = upload_file2(home_dir, mg_to_analyze)
        upload_location = synbio
        move_files_to_folder(file_paths, upload_location)

        os.chdir(synbio) 
        diamond_syn = diamond_impl(synbio, name) #diamond_syn = synbio
        output2 = genome_extractor(diamond_syn, name, home_dir)

        for item in os.listdir(synbio):
            if item.endswith('_profile'):
                source = os.path.join(synbio, item)
                destination = os.path.join(functional_folder, item)
                shutil.move(source, destination)

    #____________________________________________________________________________________#Distance Scoring
        synbio_binary = '/home/anna/Documents/JGI_soil_genomes/functional_profiles/Synbio_functional_profile'
        [distance_list_for_synbio, new_loc ]= pass_to_distance(synbio_binary, name, desired_location2, mg_to_analyze)
        st.write(mg_to_analyze + ':green[Synbio Analysis Complete]')

#     elif mg_to_analyze == 'wwtp':
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

#         # # Example usage
#         file_paths = upload_file(home_dir, mg_to_analyze)
#         upload_location = IW
#         move_files_to_folder(file_paths, upload_location)

#     ##__________________________________________________________________________________#Diamond Analysis
#         os.chdir(home_dir)
#         if os.path.exists(metagenome_name):
#             shutil.rmtree(metagenome_name)
#             os.mkdir(metagenome_name)
#         else:
#             os.mkdir(metagenome_name)
#         # home_dir = home_dir + "/" + metagenome_name 

#         os.chdir(IW)
#         diamond = diamond_impl(IW, '') #-> Takes in the path and directory
#     # #________________________________________________________________________________# Creating reference functional profile

#         dmnd_folder = '/home/anna/Documents/JGI_soil_genomes/reference_diamond_analysis_output'
#         ff_name = 'functional_profiles'
#         functional_folder = '/home/anna/Documents/JGI_soil_genomes/functional_profiles'
#         name = mg_to_analyze + '_metagenome'

#         for item in os.listdir(IW):
#             if item.endswith(('_matches.tsv', '.dmnd')):
#                 source = os.path.join(IW, item)
#                 destination = os.path.join(dmnd_folder, item)
#                 shutil.move(source, destination)
        

#         output = genome_extractor(dmnd_folder, name, home_dir)

#         os.chdir(home_dir)
#         if os.path.exists(functional_folder):
#             shutil.rmtree(functional_folder)
#             os.mkdir(ff_name)
#         else:#makes a new directory called metagenome_name
#             os.mkdir(ff_name)

#         for item in os.listdir(dmnd_folder):
#             if item.endswith('_profile'):
#                 source = os.path.join(dmnd_folder, item)
#                 destination = os.path.join(functional_folder, item)
#                 shutil.move(source, destination)
            
#     #-----------------------------------------------------------------------------------# Organism to analyze matches and functional profile creation 
#         synbio = '/home/anna/Documents/JGI_soil_genomes/' + mg_to_analyze + '_synbio_inputs_and_outputs'
#         name = 'Synbio'
#         syn_folder_name = mg_to_analyze + '_synbio_inputs_and_outputs'
#         desired_location2 = '/home/anna/Documents/JGI_soil_genomes'

#         os.chdir(home_dir)
#         if os.path.exists(synbio):
#             print('Synbio directory already exists')
#         else:#makes a new directory called metagenome_name
#             os.mkdir(syn_folder_name)

#         file_paths = upload_file2(home_dir, mg_to_analyze)
#         upload_location = synbio
#         move_files_to_folder(file_paths, upload_location)

#         os.chdir(synbio) 
#         diamond_syn = diamond_impl(synbio, name) #diamond_syn = synbio
#         output2 = genome_extractor(diamond_syn, name, home_dir)

#         for item in os.listdir(synbio):
#             if item.endswith('_profile'):
#                 source = os.path.join(synbio, item)
#                 destination = os.path.join(functional_folder, item)
#                 shutil.move(source, destination)
                
#         synbio_binary = '/home/anna/Documents/JGI_soil_genomes/functional_profiles/Synbio_functional_profile'
#         [distance_list_for_synbio, new_loc ]= pass_to_distance(synbio_binary, name, desired_location2, mg_to_analyze)
#         print(mg_to_analyze + ' vs. Synbio Analysis Complete')

#     elif mg_to_analyze == 'river':

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

#         # # Example usage
#         file_paths = upload_file(home_dir, mg_to_analyze)
#         upload_location = IW
#         move_files_to_folder(file_paths, upload_location)

#     ##__________________________________________________________________________________#Diamond Analysis
#         os.chdir(home_dir)
#         if os.path.exists(metagenome_name):
#             shutil.rmtree(metagenome_name)
#             os.mkdir(metagenome_name)
#         else:
#             os.mkdir(metagenome_name)
#         # home_dir = home_dir + "/" + metagenome_name 

#         os.chdir(IW)
#         diamond = diamond_impl(IW, '') #-> Takes in the path and directory
#     # #________________________________________________________________________________# Creating reference functional profile

#         dmnd_folder = '/home/anna/Documents/JGI_soil_genomes/reference_diamond_analysis_output'
#         ff_name = 'functional_profiles'
#         functional_folder = '/home/anna/Documents/JGI_soil_genomes/functional_profiles'
#         name = mg_to_analyze + '_metagenome'

#         for item in os.listdir(IW):
#             if item.endswith(('_matches.tsv', '.dmnd')):
#                 source = os.path.join(IW, item)
#                 destination = os.path.join(dmnd_folder, item)
#                 shutil.move(source, destination)
        

#         output = genome_extractor(dmnd_folder, name, home_dir)

#         os.chdir(home_dir)
#         if os.path.exists(functional_folder):
#             shutil.rmtree(functional_folder)
#             os.mkdir(ff_name)
#         else:#makes a new directory called metagenome_name
#             os.mkdir(ff_name)

#         for item in os.listdir(dmnd_folder):
#             if item.endswith('_profile'):
#                 source = os.path.join(dmnd_folder, item)
#                 destination = os.path.join(functional_folder, item)
#                 shutil.move(source, destination)
            
#     #-----------------------------------------------------------------------------------# Organism to analyze matches and functional profile creation 
#         synbio = '/home/anna/Documents/JGI_soil_genomes/' + mg_to_analyze + '_synbio_inputs_and_outputs'
#         name = 'Synbio'
#         syn_folder_name = mg_to_analyze + '_synbio_inputs_and_outputs'
#         desired_location2 = '/home/anna/Documents/JGI_soil_genomes'

#         os.chdir(home_dir)
#         if os.path.exists(synbio):
#             print('Synbio directory already exists')
#         else:#makes a new directory called metagenome_name
#             os.mkdir(syn_folder_name)

#         file_paths = upload_file2(home_dir, mg_to_analyze)
#         upload_location = synbio
#         move_files_to_folder(file_paths, upload_location)

#         os.chdir(synbio) 
#         diamond_syn = diamond_impl(synbio, name) #diamond_syn = synbio
#         output2 = genome_extractor(diamond_syn, name, home_dir)

#         for item in os.listdir(synbio):
#             if item.endswith('_profile'):
#                 source = os.path.join(synbio, item)
#                 destination = os.path.join(functional_folder, item)
#                 shutil.move(source, destination)
                
#         synbio_binary = '/home/anna/Documents/JGI_soil_genomes/functional_profiles/Synbio_functional_profile'
#         [distance_list_for_synbio, new_loc ]= pass_to_distance(synbio_binary, name, desired_location2, mg_to_analyze)
#         print(mg_to_analyze + ' vs. Synbio Analysis Complete')

    else:
        pass