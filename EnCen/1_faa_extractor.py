### Extracts all files from .tar compressed files. /
# parent directory is the folder the extracted file is in 
# This script is to be used before directory_clear.py



import os
import tarfile


def tar_extraction(parent_folder):
    # References those files that are compressed
    extension = ".tar.gz"
    os.chdir(parent_folder)
    # Iterates through the protein file folder, destination where the .faa files were downloaded
    for item in os.listdir(parent_folder):
        filepath = os.path.join(parent_folder, item)
        # Check for ".gz" extension, does not apply to those files that were already extracted
        if item.endswith(extension):
            print('File Found, Beginning Extraction')
            print(item)
            with tarfile.open(filepath, 'r:gz') as tar:
            # Extract all contents of the archive
                tar.extractall(path=parent_folder)
            os.remove(filepath)



# parent_folder = '/home/anna/Documents/EnCen_JGI_Genomes'
parent_folder = '/home/anna/Documents/JGI_soil_genomes/Test MGBs'
tar_extraction(parent_folder)