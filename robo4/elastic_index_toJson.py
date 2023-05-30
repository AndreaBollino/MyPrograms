import requests
import json
import time
from elasticsearch import Elasticsearch

#target_id = '2422'
file_prefix = 'bsrobo4-risp-picking-'
input_path = 'C:/Users/S511480/Desktop/Python_MieProgrammi/MyPrograms/robo4/input/'
ouput_path = 'C:/Users/S511480/Desktop/Python_MieProgrammi/MyPrograms/robo4/output/'
#input_path = 'input/'
#ouput_path = 'output/'


def login():
    url = 'https://idpint.sum.gmps.global/sbopenamrest/api/oidcappservice'
    headers = {'Content-Type': 'application/json'} 
    data = {
        "username":"APPWVELK",
        "password":"1_h849fnZuiNKocUhXDu5J9w==",
        "clientid":"digitaladv",
        "clientsecret":"1_wItFnJhk211TKX/WalIQ9A==",
        "fgPswEncrypted":"true"
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

indice = input("Inserisci indice: ") 
target_id=indice
indice = "bsrobo4-risp-picking-"+ indice

es=Elasticsearch("https://digitaladvisory-elk-wvk8snpwaelasticsearch-sysprod.apps.fi1.paas.gmps.global",headers=headers,verify_certs=False)
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
response_pit = es.open_point_in_time(index=indice,keep_alive="2m")
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

response_search = es.search(body)
hits = response_search['hits']['hits']
sort=hits[-1]['sort']
sort0=sort[0]
sort1=sort[1]

# with open("bsrobo4-risp-picking-2422-1.json", "a") as file:
#         json.dump(response_search, file)
#         file.write("\n")

with open(f'{input_path}{file_prefix}{target_id}'+'-1.json', "w") as file:
        json.dump(response_search, file)
        file.write("\n")



#IMPOSTARE CICLO
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
   
print("finito")

# Ottenere la lista dei nomi degli indici
#response = es.cat.indices(format='json')

# Estrazione dei nomi degli indici
#index_names = [index['index'] for index in response]
#print(index_names)