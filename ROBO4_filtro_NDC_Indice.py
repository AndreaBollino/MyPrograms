#elasticsearch costruisci query terms in and multisearch
#importiamo la libreria pandas per leggere i fogli excel
#scrivi programma python per chiamata rest post  di esempio con body in formato json
#scrivi programma python che ellimina " da una stringa 
#in python come posso cercare il valore di un campo nella response di una chimata rest?

#conda install -c anaconda pandas
import pandas as pd 
import requests
import json
import numpy as np
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

def countNDCad1(jwt):
    url = 'https://digitaladvisory-elk.mps.apps.paas.gmps.global:443/bsrobo4-risp-picking-'+indice+'/_count'
    autorization = 'Bearer'+ jwt
    autorization = autorization.replace('"', '')
    autorization = autorization.replace('}', '')
    #print(autorization)
    headers = {'Content-Type': 'application/json','Authorization': autorization} 
    #print (headers)
    data = {"query":{"term":{"strategiaAssegnata":{"value":"1"}}}}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    #print('INDICE: ' + response.text)
    data2 = json.loads(response.text)
    value = data2['count']
    #print('Numero NDC con Strategia ad 1 su INDICE: ' + str(value))
    return value
    
def countPresenti(jwt,listaXLS):
    url = 'https://digitaladvisory-elk.mps.apps.paas.gmps.global:443/bsrobo4-risp-picking-'+indice+'/_count'
    autorization = 'Bearer'+ jwt
    autorization = autorization.replace('"', '')
    autorization = autorization.replace('}', '')
    #print(autorization)
    headers = {'Content-Type': 'application/json','Authorization': autorization} 
    #print (headers)
    #https://stackoverflow.com/questions/43633472/how-to-simulate-multiple-fields-in-a-terms-query
    data ={ 
    "query": { 
        "bool": { 
            "must": [ 
                {"term": {"strategiaAssegnata":{"value":"1"}}}, 
                {"terms": {"ndg": listaXLS}}
            ] 
        } 
    } 
}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    #data2 = response.json() 
    data2 = json.loads(response.text)
    value = data2['count']
    #print('Presenza NDC da foglio xls su INDICE e strategia ad 1: ' + str(value))
    return value
def updateNDCstrategiaNULL(listaxls):
    #url = 'https://digitaladvisory-elk.coding.mps.apps.paas.testfactory.copergmps:443/bsrobo4-risp-picking-'+indice+'/_update_by_query'
    url = 'https://digitaladvisory-elk.mps.apps.paas.gmps.global:443/bsrobo4-risp-picking-'+indice+'/_update_by_query'
    autorization = 'Bearer'+ jwt
    autorization = autorization.replace('"', '')
    autorization = autorization.replace('}', '')
    #print(autorization)
    headers = {'Content-Type': 'application/json','Authorization': autorization} 
    #print (headers)
    data ={
    "script": {
        "source": "ctx._source.strategiaAssegnata = null",
        "lang": "painless"
     },
    "query": {
        "terms": {"ndg": listaxls}
     }
    }
    #try: 
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    #except requests.exceptions.RequestException as e: 
    #    print('An exception has occurred: %s' % e)
    #print('INDICE: ' + response.text)
    #data2 = response.json() 
    #value = data2['count']
    print('NDC da lista xls messi Strategia a null: ' + str(response))
    return response.status_code

indice=input("Immetti numero indice : ")   
indice = str(indice)       
jwt = login()
countNDCad1SuIndice = countNDCad1(jwt)
print (countNDCad1SuIndice)
#updateNDCstrategiaNULL()
filexls = input("Immetti nome folgio xls filtro : ")  

#data = pd.read_excel('CA Fondi Finestra_bsrobo4-risp-picking-1669 - esclusioni.xlsx') 
data = pd.read_excel(filexls) 
lista = data.iloc[:,0].tolist() 
lista[:] = np.unique(lista)
output = [str(x) for x in lista]
outputOrig = [str(x) for x in lista]
#per ogni elemento della lista, sostituiamolo con se stesso concatenato con +
risposta= input('vuoi preparare file txt con NDC pronti per Postman? s/n ')
if (risposta=='s'):
    with open('modificato.txt', 'w') as outfile:
        for i in range(len(output)-1):  #scorriamo tutti gli elementi della lista  
            output[i] = '"' + output[i] + '"' + ',' #sostituisci l'elemento con se stesso concatenato con +  
            print(output[i])
            outfile.write(output[i]+"\n")

        output[len(output)-1] = '"' + output[len(output)-1] + '"' 
        print(output[len(output)-1])
        outfile.write(output[len(output)-1])
        #print(len(output))
        outfile.close()
ciccio= input('vai avanti')
countNDCxlsStr1 = countPresenti(jwt,outputOrig)
print('Presenza NDC su INDICE e strategia ad 1: ' + str(countNDCad1SuIndice))
print('NDC da elliminare: ' + str(len(outputOrig)))
print('Presenza NDC da foglio xls su INDICE e strategia ad 1: ' + str(countNDCxlsStr1))
print('NDC rimanenti dopo aver Filtrato= ' + str(countNDCxlsStr1-len(outputOrig)))
pippo=input('Dai ok per update')
try:
    risposta = updateNDCstrategiaNULL(outputOrig)
except requests.exceptions.RequestException as e: 
    print('An exception has occurred: %s' % e)
    print('Presenza NDC da foglio xls su INDICE e strategia ad 1: ' + str(countPresenti(jwt,outputOrig)))
    print('Presenza NDC su INDICE e strategia ad 1: ' + str(countNDCad1(jwt)))
    esci=input()
    exit()
if (risposta == 200):
    print('UPDATE eseguito messa strategia a null su NDC dell Indice presenti in foglio xls')
    print('Presenza NDC da foglio xls su INDICE e strategia ad 1: ' + str(countPresenti(jwt,outputOrig)))
    print('Presenza NDC su INDICE e strategia ad 1: ' + str(countNDCad1(jwt)))
else:
    ndcAD1 = countPresenti(jwt,outputOrig)
    while ndcAD1 != 0: 
            print('Presenza NDC da foglio xls su INDICE e strategia ad 1: ' + str(ndcAD1))
            time.sleep(10)
            ndcAD1 = countPresenti(jwt,outputOrig)

print('UPDATE eseguito messa strategia a null su NDC dell Indice presenti in foglio xls')
print('Presenza NDC da foglio xls su INDICE e strategia ad 1: ' + str(countPresenti(jwt,outputOrig)))
print('Presenza NDC su INDICE e strategia ad 1: ' + str(countNDCad1(jwt)))

esci=input()
