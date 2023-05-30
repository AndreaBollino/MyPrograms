
import pandas as pd
import json
import dask.dataframe as dd
import numpy as np
import zipfile
import glob
import numba
import os

import elementpath
from xml.etree import ElementTree
import numpy as np
pd.options.display.max_columns = 999

target_id = '2'
file_prefix = 'bsrobo4-risp-picking-'
input_path = 'C:/Users/magagnolif/Desktop/Materiale MPS/Materiale Progetti/RB4/PYTHON/input/'
ouput_path = 'C:/Users/magagnolif/Desktop/Materiale MPS/Materiale Progetti/RB4/PYTHON/output/'

#get_ipython().run_cell_magic('time', '', "df = pd.DataFrame()\n\nwith open(f'{input_path}{file_prefix}{target_id}'+'.json') as file:\n    json_data = json.load(file)\n    df_tmp = pd.DataFrame.from_records(pd.DataFrame(json_data['hits']['hits'])['_source'].values)\n    print(df_tmp)\n    df = pd.concat([df,df_tmp])\ndf = df.reset_index(drop = True)")

df = pd.DataFrame()

with open(f'{input_path}{file_prefix}{target_id}'+'.json') as file:
    json_data = json.load(file)
    df_tmp = pd.DataFrame.from_records(pd.DataFrame(json_data['hits']['hits'])['_source'].values)
    print(df_tmp)
    df = pd.concat([df,df_tmp])
df = df.reset_index(drop = True)

def extract_elements(group):
    def get_attr(el,key):
        return None if el.find(key) is None else el.find(key).text
    
    delta_plus = pd.DataFrame()
    filiale = group['filiale'].values[0]
    codiceGestore = group['codiceGestore'].values[0]
    outcome = group['outcome'].values[0]
    codiceCliente = group['codiceCliente'].values[0]
    delta_plus = pd.concat([delta_plus, pd.DataFrame([[
                                  filiale,
                                  codiceGestore,
                                  outcome,
                                  codiceCliente
                                  ]],
                                columns = [
                                           'filiale',
                                           'codiceGestore',
                                           'outcome',
                                           'codiceCliente'
                                                      ])])
    return delta_plus

output = df.groupby('codiceCliente').apply(extract_elements).reset_index(drop = True)
#output = df.apply(extract_elements).reset_index(drop = True)
output.to_csv(f'{ouput_path}bsrobo4-risp-picking-{target_id}.csv',sep= ';', index = False)

input_files = os.listdir(f'{input_path}')
print(input_files)
for inputf in input_files:
    if(inputf.find('bsrobo4-risp-picking-') == -1):
        continue
    target_id = inputf.replace('bsrobo4-risp-picking-','').replace('.zip','');
    print('processing target_id'+target_id)



