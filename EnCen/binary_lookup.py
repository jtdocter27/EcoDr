import pandas as pd 

synbio_binary = '/home/anna/Desktop/vn uneditted func prof'
EC = '1.1.1.1'

synbio_binary = pd.read_csv(synbio_binary, delimiter=" ", header=0)
# print(type(synbio_binary))
# synbio_binary = synbio_binary.set_index('Name_of_MetaGenome_Bin')
# print(synbio_binary)
transpose = synbio_binary.transpose()
# print(transpose) #fuckin bingo 
# print(transpose.index)
value = int(transpose.loc[EC])
print(value)

###Second Profile_______________________________________________________________________
synbio_binary_edited = '/home/anna/Desktop/vn w but genes func prof'
synbio_binary_edited = pd.read_csv(synbio_binary_edited, delimiter=" ", header=0)

transpose2 = synbio_binary_edited.transpose()
# print(transpose) #fuckin bingo 
# print(transpose.index)
value2 = int(transpose2.loc[EC])
print(value2) 

if value == value2: 
    print("enzyme did not flip")
else:
    print('enzyme flipped')