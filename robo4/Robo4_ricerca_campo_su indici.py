from elasticsearch import Elasticsearch
import requests
import json
from elasticsearch import Elasticsearch
import os
import getpass

# Connect to Elasticsearch
es = Elasticsearch()

# Search for indices

user = os.environ.get("USERNAME")
print ("Utente: "+user)
passwd = getpass.getpass("Inserisci la tua password: ")

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

es=Elasticsearch("https://digitaladvisory-elk-wvk8snpwaelasticsearch-sysprod.apps.fi1.paas.gmps.global",headers=headers,verify_certs=False,timeout=30)


indices = es.indices.get_alias("bsrobo4-risp-picking-*")

# Check each index for the "familyStrategyCode" field
""" for index in indices:
    mapping = es.indices.get_mapping(index=index)
    properties = mapping[index]['mappings']['properties']
    if 'familyStrategyCode' in properties and properties['familyStrategyCode']['type'] == 'text' and properties['familyStrategyCode']['fields']['keyword']['ignore_above'] == 256 and properties['familyStrategyCode']['fields']['keyword']['type'] == 'keyword':
        if properties['familyStrategyCode']['fields']['keyword']['normalizer'] == 'lowercase':
            print("Trovato") """
indices = list(indices.keys())
query = {
        "query": {
            "match": {
                "familyStrategyCode": "CA - Sottopeso obbligazionario"
            }
        }
    }
for index in indices:
 result = es.search(index=index, body=query)
 if result['hits']['total']['value'] > 0:
        indice = result['hits']['hits'][0]['_index']
        print(result['hits']['hits'][0]['_index'])
        indiceD = index
        print(index)
        familyStrategyCode = result['hits']['hits'][0]['_source']['familyStrategyCode']
        print(result['hits']['hits'][0]['_source']['familyStrategyCode'])
        ndg = result['hits']['hits'][0]['_source']['ndg']
        print(result['hits']['hits'][0]['_source']['ndg'])
        

print (indice)
print (indiceD)
print (familyStrategyCode)
print (ndg)
 #print(result['hits']['hits']['_index'])

#if result['hits']['hits']['_index']['ctvTot'] > 0:
        #print(result['hits']['total']['value'])
