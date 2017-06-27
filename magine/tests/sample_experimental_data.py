import os

from magine.data.datatypes import ExperimentalData

data_dir = os.path.dirname(__file__)
exp_data = ExperimentalData(data_file='example_apoptosis.csv',
                            data_directory=os.path.join(data_dir, 'Data'))
