import pandas as pd



kleb = pd.read_csv('/home/anna/Downloads/kleb_funct_profile', delimiter = ' ')
klbe2 = kleb.T
# print(klbe2)
new_header = klbe2.iloc[0]
kleb3 = klbe2[1:]
kleb3.columns=new_header


Paen = pd.read_csv('/home/anna/Desktop/planticola.txt', delimiter = ' ')
paen2 = Paen.T
new_header2 = paen2.iloc[0]
paen3 = paen2[1:]
paen3.columns=new_header2
pane4 = paen3.rename(columns={'Synbio_matches.tsv': 'panticola'})
print(pane4.columns)

combined = pd.concat([kleb3, pane4], axis = 1)
print(combined.columns)

# combined.to_excel('Combined.xlsx')
# reset = combined.reset_index
# print(reset)
print(len(combined.query('`Synbio_matches.tsv` == panticola')))

