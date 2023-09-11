#pyinstaller --onefile prova.py  //per generare .exe
#query associazione nome strategia indice ROBO in fondo al codice
import requests
import json
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
import glob
import elementpath
import os
import getpass
import pprint

from xml.etree import ElementTree
import numpy as np
import cx_Oracle

pd.options.display.max_columns = 999

file_prefix = 'bsrobo4-risp-picking-'
#input_path = 'C:/Users/S511480/Desktop/Python_MieProgrammi/MyPrograms/robo4/input/'
#ouput_path = 'C:/Users/S511480/Desktop/Python_MieProgrammi/MyPrograms/robo4/output/'

#env_var = os.environ 
# Print the list of user's
# environment variables
#print("User's Environment variable:")
#print(dict(env_var))


#user = input("Inserire utente (SXXXXXX): ")
user = os.environ.get("USERNAME")
print ("Utente: "+user)
passwd = getpass.getpass("Inserisci la tua password: ")
#print("La password inserita è:", pw)

cx_Oracle.init_oracle_client(config_dir="C:\\oracle\\ora12R2CL_32\\network\\admin")
connection = cx_Oracle.connect(dsn="OraWV_NPWAADVISORYAPP_PROD.world", encoding="UTF-8")
sessione = input("Inserisci descrizione sessione: ")
sessione = "%"+sessione+"%"
cursor = connection.cursor()
query = """
WITH totale AS
  (SELECT r4s.DESCRIPTION AS R4_SESSION_DESCRIPTION,
    s.INDICE_OUTPUT       AS BS_SESSION_SCHED_INDICE_OUTPUT,
    r4t.id                AS R4_TARGET_ID,
    bsw.START_DATE        AS data_partenza
  FROM NPWACDR4.BS_SESSION_SCHED s
  INNER JOIN Npwacdr4.Bs_Session_Progress P
  ON P.Id_Session_Sched = S.Id
  LEFT JOIN NPWACDR4.R4_TARGET r4t
  ON r4t.id = s.CODICE_SESSIONE
  LEFT JOIN NPWACDR4.R4_SESSION r4s
  ON r4s.id = r4t.SESSION_ID
  JOIN NPWACDR4.BS_SESSION_WORKER_PROGRESS bsw
  ON p.id              = bsw.ID_SESSION_PROGRESS
  WHERE 1              =1
  AND r4s.DESCRIPTION IS NOT NULL
  --AND R4s.Description LIKE 'CA Top di Gamma Aderenza < 7 LUG-AGO 23'
  AND R4s.Description LIKE :description
    --and s.INDICE_OUTPUT  in ('bsrobo4-risp-picking-2507','bsrobo4-risp-picking-2506')
    --order by r4t.id desc-- as R4_TARGET_ID
  ORDER BY bsw.START_DATE DESC
  )
SELECT R4_SESSION_DESCRIPTION,
  BS_SESSION_SCHED_INDICE_OUTPUT,
  R4_TARGET_ID
FROM totale
GROUP BY R4_SESSION_DESCRIPTION,
  BS_SESSION_SCHED_INDICE_OUTPUT,
  R4_TARGET_ID
"""
cursor.execute(query, description=sessione)
#cursor.execute(query)

# Recupero dei risultati
#results = cursor.fetchall()
# Ottenimento dei risultati univoci
distinct_results = set()
for row in cursor:
    distinct_results.add(row)

indice = None
if distinct_results:
    indice = list(distinct_results)[-1][-1]

# Stampa del risultato
print("Valore dell'ultima colonna (indice):", indice)
indice = str(indice)
# Chiusura della connessione
cursor.close()
connection.close()

def login():
    url = 'https://idpint.sum.gmps.global/sbopenamrest/api/oidcappservice'
    headers = {'Content-Type': 'application/json'} 
    data = {
        #"username":"APPWVELK",
        "username":user,
        #"password":"1_h849fnZuiNKocUhXDu5J9w==",
        "password":passwd,
        "clientid":"digitaladv",
        "clientsecret":"1_wItFnJhk211TKX/WalIQ9A==",
        #"fgPswEncrypted":"true"
        "fgPswEncrypted":"false",
        "scope":"roles"
}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    jwt=response.text.split(':')[1]
    print('JWT:' + jwt)
    pprint.pprint('JWT:' + jwt)
    return jwt


jwt = login()
	

autorization = 'Bearer'+ jwt
autorization = autorization.replace('"', '')
autorizationNew = autorization.replace('}', '')

authorization = autorizationNew # Inserisci il tuo token di autorizzazione

# Intestazioni per la chiamata Elasticsearch
headers = {
    'Content-Type': 'application/json',
    'Authorization': authorization
}

#indice = input("Inserisci indice: ")
robo_path = input("Inserisci path nel formato es C:\\Users\\S511480\\Desktop\\robo4 : ")
input_path = robo_path+'\\input'
ouput_path = robo_path+'\\output'
#input_path = os.path.dirname(os.path.abspath(__file__))+'\\input'
#ouput_path = os.path.dirname(os.path.abspath(__file__))+'\\output'

if not os.path.exists(input_path+"\\bsrobo4-risp-picking-"+ indice):
        os.makedirs(input_path+"\\bsrobo4-risp-picking-"+ indice)
if not os.path.exists(ouput_path+"\\bsrobo4-risp-picking-"+ indice):
        os.makedirs(ouput_path+"\\bsrobo4-risp-picking-"+ indice)

input_path = input_path+"\\bsrobo4-risp-picking-"+ indice+"\\"
ouput_path = ouput_path+"\\bsrobo4-risp-picking-"+ indice+"\\"

target_id=indice
target_id2=indice
indice = "bsrobo4-risp-picking-"+ indice

es=Elasticsearch("https://digitaladvisory-elk-wvk8snpwaelasticsearch-sysprod.apps.fi1.paas.gmps.global",headers=headers,verify_certs=False,timeout=30)
#es=Elasticsearch("https://digitaladvisory-elk.mps.apps.paas.gmps.global",headers=headers,verify_certs=False)
#es.info()
body = {
    "query": {
        "term": {
            "strategiaAssegnata": {
                "value": "1"
            }
        }
    }
}

# Esegui la ricerca
response_count = es.count(index=indice, body=body)
# Ottieni il numero di risultati
count = response_count['count']
print("Numero di risultati: ", count)

pagination_size = int(input("Inserisci numero documenti per pagina (file json): "))

#response = es.pit(params={"keep_alive": "1m"})
response_pit = es.open_point_in_time(index=indice,keep_alive="10m")
print(response_pit['id'])


body = {
    "query": {
        "term": {
            "strategiaAssegnata": {
                "value": "1"
            }
        }
    },
    "_source": False,
    "fields": [
        "ndg",
        "modelloServizio",
        "mercato",
        "filialeGui",
        "codiceGestoreGui",
        "valoreAderenzaSimulato",
        "deltaAderenza",
        "codiceCliente",
        "ctvAllocatoSimulato",
        "ctvTot",
        "familyStrategyCode",
        "familyStrategyScope",
        "richiesta51316ResponseXML"
    ],
    "size": pagination_size,
    "pit": {
        "id": response_pit['id']   
        },
    "sort": [
        {
            "_id": {
                "order": "asc"
            }
        },
        {
            "_shard_doc": "desc"
        }
    ]
}

response_search = es.search(body,request_timeout=30)
hits = response_search['hits']['hits']
sort=hits[-1]['sort']
sort0=sort[0]
sort1=sort[1]

with open(f'{input_path}{file_prefix}{target_id}'+'-1.json', "w") as file:
        json.dump(response_search, file)
        file.write("\n")

#IMPOSTARE CICLO  da JMeter
# int totalIterations=${count}/${pagination-size};
# int totalpages=totalIterations+2;
# vars.put("start",""+2);
# vars.put("total-pages",""+totalpages);
# vars.put("total-iterations",""+totalIterations)
totalIterations = count//pagination_size

counter = 2
while counter < (totalIterations+2):
   print(counter)
   body = {
        "query": {
            "term": {
                "strategiaAssegnata": {
                    "value": "1"
                }
            }
        },
        "_source": False,
        "fields": [
        "ndg",
            "modelloServizio",
            "mercato",
            "filialeGui",
            "codiceGestoreGui",
            "valoreAderenzaSimulato",
            "deltaAderenza",
            "codiceCliente",
            "ctvAllocatoSimulato",
            "ctvTot",
            "familyStrategyCode",
            "familyStrategyScope",
            "richiesta51316ResponseXML"
        ],
        "size": pagination_size,
        "pit": {
            "id": response_pit['id']
            },
        "sort": [
            {
                "_id": {
                    "order": "asc"
                }
            },
            {
                "_shard_doc": "desc"
            }
        ],
        "search_after": [
            sort0,
            sort1
        ]
    }

   response_search = es.search(body)
   hits = response_search['hits']['hits']
   sort=hits[-1]['sort']
   sort0=sort[0]
   sort1=sort[1]

   with open(f'{input_path}{file_prefix}{target_id}'+'-'+str(counter)+'.json', "w") as file:
            json.dump(response_search, file)
            file.write("\n")
   counter += 1
print("Finita parte creazione Json")
#print("Si può scegliere creazione unico csv dando invio")
#print("Inserire indice intero oppure con ""-numero"" in base alla creazioe dei json")

#target_id = input("Inserire indice intero oppure con ""-numero"" in base alla creazioe dei json: ") 
#if len(target_id) == 0:
target_id=target_id2

listFile = glob.glob(f'{input_path}{file_prefix}{target_id}*')
print(listFile)

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

print("finito csv nella cartella output ")

""" select 
r4s.DESCRIPTION as R4_SESSION_DESCRIPTION,
s.INDICE_OUTPUT as BS_SESSION_SCHED_INDICE_OUTPUT,
r4t.id as R4_TARGET_ID,
s.id as BS_SESSION_SCHED_ID,
s.CODICE_SESSIONE as BS_SESSION_SCHED_CODICE_SESSIONE,
s.STATO as BS_SESSION_SCHED_STATO,
p.id as Bs_Session_Progress_ID,
P.ID_SESSION_SCHED as Bs_Session_Progress_ID_SESSION_SCHED,

r4t.SESSION_ID as R4_TARGET_SESSION_ID,
r4s.ID as R4_SESSION_ID,
r4s.PHASE as R4_SESSION_PHASE,
r4s.STATUS as R4_SESSION_STATUS,
'BS_SESSION_WORKER_PROGRESS --->',
bsw.*

FROM NPWACDR4.BS_SESSION_SCHED s
INNER JOIN Npwacdr4.Bs_Session_Progress P
ON P.Id_Session_Sched = S.Id
LEFT JOIN NPWACDR4.R4_TARGET r4t
ON r4t.id = s.CODICE_SESSIONE
LEFT JOIN NPWACDR4.R4_SESSION r4s
ON r4s.id = r4t.SESSION_ID
join NPWACDR4.BS_SESSION_WORKER_PROGRESS bsw
on p.id = bsw.ID_SESSION_PROGRESS
WHERE 1=1
and r4s.DESCRIPTION is not null
--and R4s.Description like 'CA Personal Style Mag 23'
order by r4t.id desc-- as R4_TARGET_ID
--order by bsw.START_DATE desc """

