import requests
import json
import time

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
base_url = 'https://digitaladvisory-elk.mps.apps.paas.gmps.global:443/'
#base_url = 'https://digitaladvisory-elk.coding.mps.apps.paas.testfactory.copergmps:443/'

# Intestazioni per la richiesta delete
# headers = {
    # 'Content-Type': 'application/json',
    # 'Authorization': authorization
# }

autorization = 'Bearer'+ jwt
autorization = autorization.replace('"', '')
autorization = autorization.replace('}', '')
    #print(autorization)
headers = {'Content-Type': 'application/json','Authorization': autorization} 

# Lettura della lista di indici dal file txt
with open('indici_da_cancellare.txt', 'r') as index_file:
    indices = index_file.readlines()


indices[:] = list(set(indices))



# Rimozione degli indici su Elasticsearch
for index in indices:
    index = index.strip()  # Rimuove spazi bianchi e caratteri di nuova riga
    delete_url = base_url + index
    response = requests.delete(delete_url, headers=headers,verify=False)

    if response.status_code == 200:
        print(f"Indice '{index}' cancellato con successo.")
    else:
        print(f"Errore durante la cancellazione dell'indice '{index}'."
              f" Codice di risposta: {response.status_code}")