import numpy as np
import pandas as pd

from Mappings.maps import human_uniprot_to_gene_name

proteins = []
for each in human_uniprot_to_gene_name.values():
    for j in each:
        proteins.append(j)
proteins = set(proteins)
hmdb = pd.read_pickle('../hmdb_dataframe.p')
hmdb.set_index('name').to_dict()
hmdb.name = map(lambda x: x.upper(), hmdb.name)

# names = hmdb.keys()
names = dict(zip(hmdb.name, hmdb.accession))


# print(names)
def extract_humancyc():
    data = np.loadtxt('HumanCyc_metabolic_pathways.sif', delimiter='\t', dtype=str)
    data[:, 0] = map(lambda x: x.upper(), data[:,0])

    data[:, 2] = map(lambda x: x.upper(), data[:, 2])
    int_types = ['neighbor-of', 'catalysis-precedes', 'in-complex-with', 'consumption-controlled-by',
                 'controls-production-of', 'used-to-produce', 'reacts-with', 'controls-state-change-of',
                 'controls-transport-of-chemical', 'chemical-affects']
    unknowns = []
    counter = 0
    for i in range(len(data)):
        if data[i, 1] == 'controls-production-of':
            if data[i,0] in names:
                counter += 1
                print('hello', names[data[i, 0]], data[i, 0])
            else:
                unknowns.append(data[i,0])
            if data[i, 2] in names:
                counter += 1
                print('hello2', names[data[i, 2]], data[i, 2])
            else:
                unknowns.append(data[i, 2])
    unknowns = set(unknowns)
    print(len(unknowns))
    counter2 = 0
    unknown_still = []
    for i in unknowns:
        if i in proteins:
            counter2 += 1
        else:
            unknown_still.append(i)
    print('Found protein names for = %i' % counter2)
    print('Found HMDB ids for= %i' % counter)
    print('Unknown ids = %i' % len(unknown_still))
    for i in unknown_still:
        print(i)
extract_humancyc()