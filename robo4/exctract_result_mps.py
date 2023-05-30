
import pandas as pd
import json
import dask.dataframe as dd
import numpy as np
import zipfile
import glob
import numba

import elementpath

#pyinstaller --onefile prova.py  //per generare .exe

from xml.etree import ElementTree
import numpy as np
pd.options.display.max_columns = 999

target_id = input("Inserisci indice con eventuale - : ") 

#target_id = '2413'
file_prefix = 'bsrobo4-risp-picking-'
#input_path = 'C:/Users/magagnolif/Desktop/Materiale MPS/Materiale Progetti/RB4/PYTHON/input/'
#ouput_path = 'C:/Users/magagnolif/Desktop/Materiale MPS/Materiale Progetti/RB4/PYTHON/output/'
input_path = 'C:/Users/S511480/Desktop/Python_MieProgrammi/MyPrograms/robo4/input/'
ouput_path = 'C:/Users/S511480/Desktop/Python_MieProgrammi/MyPrograms/robo4/output/'

listFile = glob.glob(f'{input_path}{file_prefix}{target_id}*')
print(listFile)
#archive = zipfile.ZipFile(listFile[0], 'r')

#get_ipython().run_cell_magic('time', '', "df = pd.DataFrame()\n\nfor file in archive.filelist:\n    z = archive.open(file)\n    json_data = json.load(z)\n\n    df_tmp = pd.DataFrame.from_records(pd.DataFrame(json_data['hits']['hits'])['fields'].values)\n    df = pd.concat([df,df_tmp])\ndf = df.reset_index(drop = True)\n\nfor col in df.columns:\n    df[col] = df[col].apply(lambda x: x[0])")

df = pd.DataFrame()

for file in listFile:
    z = open(file)
    json_data = json.load(z)

    df_tmp = pd.DataFrame.from_records(pd.DataFrame(json_data['hits']['hits'])['fields'].values)
    df = pd.concat([df,df_tmp])
#print(df)
df = df.reset_index(drop = True)
#print(df)

for col in df.columns:
    df[col] = df[col].apply(lambda x: x[0])

#print(df)

def extract_elements(group):
    def get_attr(el,key):
        return None if el.find(key) is None else el.find(key).text
    
    delta_plus = pd.DataFrame()
    ndg = group['ndg'].values[0]
    valoreAderenzaSimulato = group['valoreAderenzaSimulato'].values[0]
    mercato = group['mercato'].values[0]
    modelloServizio = group['modelloServizio'].values[0]
    deltaAderenza = group['deltaAderenza'].values[0]
    filialeGui = group['filialeGui'].values[0]
    codiceGestoreGui = group['codiceGestoreGui'].values[0]
    delta_plus = pd.concat([delta_plus,pd.DataFrame([[
                                  ndg,
                                  valoreAderenzaSimulato,
                                  mercato,
                                  modelloServizio,
                                  deltaAderenza,
                                  filialeGui,
                                  codiceGestoreGui
                                  ]],
                                columns = [
                                           'ndg',
                                           'valoreAderenzaSimulato',
                                           'mercato',
                                            'modelloServizio',
                                            'deltaAderenza',
                                            'filialeGui',
                                            'codiceGestoreGui'
                                                      ])])
    return delta_plus

output = df.groupby('ndg').apply(extract_elements).reset_index(drop = True)
output.to_csv(f'{ouput_path}bsrobo4-risp-picking-{target_id}.csv',sep= ';', index = False)

def extract_elements_from_xml(group):
    def get_attr(el,key):
        return None if el.find(key) is None else el.find(key).text
    
    delta_plus = pd.DataFrame()
    stringa = group['richiesta51316ResponseXML'].values[0]
    
    familyStrategyCode = group['familyStrategyCode'].values[0]
    familyStrategyScope = group['familyStrategyScope'].values[0]
    ndg = group['ndg'].values[0]
    valoreAderenzaSimulato = group['valoreAderenzaSimulato'].values[0]
    root = ElementTree.XML(stringa)
    idChiamante = root.find('idChiamante').text
    for el in elementpath.select(root, 'rispostaAdeguatezza/risultatoAdeguatezza/resultControlli'):
        if get_attr(el,'codice') == 'RMMIGL_12':
            properties = elementpath.select(el, 'properties')
            for prop in properties:
                if get_attr(prop,'key') == 'VAR_NEW':
                    var_new = np.float64(get_attr(prop,'value'))
                elif get_attr(prop,'key') == 'VAR_OLD':
                    var_old = np.float64(get_attr(prop,'value'))
                elif get_attr(prop,'key') == 'SOGLIA_RM':
                    var_soglia = np.float64(get_attr(prop,'value'))
    for el in elementpath.select(root, 'rispostaPicking/ptfOut/saldi'):
            properties = elementpath.select(el, 'properties')
            for prop in properties:
                if prop.findall('key')[0].text == 'CTV_DELTA':
                    ctv_delta = float(prop.findall('value')[0].text)
                    codAggr = get_attr(el,'codAggr')
                    codInterno = get_attr(el,'codInterno')
                    codRischio = get_attr(el,'codRischio')
                    codiceBanca	= get_attr(el,'codiceBanca')
                    codiceFiliale = get_attr(el,'codiceFiliale')
                    codiceRapporto = get_attr(el,'codiceRapporto')
                    codiceTipoRapporto = get_attr(el,'codiceTipoRapporto')
                    idPortafoglioOperativo = get_attr(el,'idPortafoglioOperativo')
                    ctv_new = float(el.find('ctv').text)
                    ctv_old = ctv_new - ctv_delta
                    delta_plus = pd.concat([delta_plus,pd.DataFrame([[
                                                                      idChiamante,
                                                                      familyStrategyCode,
                                                                      familyStrategyScope,
                                                                      codAggr,
                                                                      codInterno,
                                                                      codRischio,
                                                                      codiceBanca,
                                                                      codiceFiliale,
                                                                      codiceRapporto,
                                                                      codiceTipoRapporto,
                                                                      ctv_old,
                                                                      ctv_delta,
                                                                      ctv_new,
                                                                      var_old,
                                                                      var_new,
                                                                      var_soglia
                                                                      ]],
                                                                    columns = [
                                                                               'idChiamante',
                                                                               'familyStrategyCode',
                                                                               'familyStrategyScope',
                                                                               'codAggr',
                                                                               'codInterno',
                                                                               'codRischio',
                                                                               'codiceBanca',
                                                                               'codiceFiliale',
                                                                               'codiceRapporto',
                                                                               'codiceTipoRapporto',
                                                                               'ctv_old',
                                                                               'ctv_delta',
                                                                               'ctv_new',
                                                                               'var_old',
                                                                                  'var_new',
                                                                                  'var_soglia'
                                                                                          ])])
    return delta_plus

output = df.groupby('ndg').apply(extract_elements_from_xml).reset_index(drop = True)
output.to_csv(f'{ouput_path}bsrobo4-risp-picking-{target_id}-resp.csv',sep= ';', index = False)

output['ctv_old'].describe()

output['ctv_new'].describe()





