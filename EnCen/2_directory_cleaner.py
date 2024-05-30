###This code iterates through a directory and deletes all files that are not a .faa. 
import os

def delete_files_not_ending_with(directory, extension, extension2):
    for filename in os.listdir(directory):
        if not filename.endswith((extension, extension2)):
            try:
                filepath = os.path.join(directory, filename)
                os.remove(filepath)
                print('Deleted :', filepath)
            except:
                print('Skipped over', filename)
# Provide the directory path
directory_path = '/home/anna/Documents/JGI_soil_genomes/Test MGBs/River'

# Provide the file extension you want to keep
file_extension_to_keep1 = '.faa'
file_extension_to_keep2 = 'phylodist.txt'

delete_files_not_ending_with(directory_path, file_extension_to_keep1, file_extension_to_keep2)