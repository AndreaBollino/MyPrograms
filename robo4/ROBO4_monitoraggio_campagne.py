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
indice = None
indice = input("Inserisci Indice: ")
indice = str(indice)

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
robo_path = input("Inserisci path nel formato es C:\\Users\\S511480\\Desktop\\robo4\\monitoraggio : ")
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

    df_tmp = pd.DataFrame.from_records(pd.DataFrame(json_data['hits']['hits'])['_source'].values)
    df = pd.concat([df,df_tmp])
#print(df)
df = df.reset_index(drop = True)
#print(df)

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

