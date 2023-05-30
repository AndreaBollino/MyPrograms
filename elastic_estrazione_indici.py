import requests
import json
import time
from elasticsearch import Elasticsearch

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
	
# URL di base per Elasticsearch
#base_url = 'https://digitaladvisory-elk.mps.apps.paas.gmps.global:443/'
#base_url = 'https://digitaladvisory-elk.coding.mps.apps.paas.testfactory.copergmps:443/'

# Intestazioni per la richiesta delete
# headers = {
    # 'Content-Type': 'application/json',
    # 'Authorization': authorization
# }

autorization = 'Bearer'+ jwt
autorization = autorization.replace('"', '')
autorizationNew = autorization.replace('}', '')
    #print(autorization)
#headers = {'Content-Type': 'application/json','Authorization': autorization} 

#es = Elasticsearch(['digitaladvisory-elk.mps.apps.paas.gmps.global:443'])

#host = 'digitaladvisory-elk.mps.apps.paas.gmps.global'
#host = 'https://digitaladvisory-elk.mps.apps.paas.gmps.global'
#port = 443
authorization = autorizationNew # Inserisci il tuo token di autorizzazione

# Intestazioni per la chiamata Elasticsearch
headers = {
    'Content-Type': 'application/json',
    'Authorization': authorization
}

# Connessione a Elasticsearch
#es = Elasticsearch(hosts=[{'host': host, 'port': port}], verify_certs=False)
es=Elasticsearch("https://digitaladvisory-elk.mps.apps.paas.gmps.global",headers=headers,verify_certs=False)
es.info()

# Ottenere la lista dei nomi degli indici
response = es.cat.indices(format='json')

# Estrazione dei nomi degli indici
index_names = [index['index'] for index in response]

newlist = [x for x in index_names if  x.startswith('bsrobo4-risp-picking')]
#newlist.sort()

B = []
for num in newlist:
    #per valore non per riferimento
	num = '\''+num+'\''+','
	B.append(num)
B.sort()
print(B)

# produce lo stesso risulatato dell'istruziine con ciclo for sopra devo usare nuova lista 
# i = 0
# while i < len(newlist):
#   newlist[i] = '\''+newlist[i]+'\''+',' 
#   i = i + 1
# newlist.sort()
# print(newlist)

# Scrivi i nomi degli indici su un file
with open('nomi_indici_per_quey.txt', 'w') as file:
   file.write('\n'.join(B))