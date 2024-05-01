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




            # try:
            # # Finds full path of files
            #     gz_name = os.path.abspath(item)
            # # Finds file name for file within, GCF and ASM names
            #     print(file_name)
            #     with gzip.open(gz_name, "rb") as f_in, open(file_name, "wb") as f_out:
            #         shutil.copyfileobj(f_in, f_out)
            #     os.remove(gz_name)  # delete zipped filep
            # except Exception as e:
                # print('GZIP fucked')

# parent_folder = '/home/anna/Documents/EnCen_JGI_Genomes'
parent_folder = '/home/anna/Documents/Soil_extracted_genomes'
tar_extraction(parent_folder)