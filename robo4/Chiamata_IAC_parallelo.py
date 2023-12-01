#elasticsearch costruisci query terms in and multisearch
#importiamo la libreria pandas per leggere i fogli excel
#scrivi programma python per chiamata rest post  di esempio con body in formato json
#scrivi programma python che ellimina " da una stringa 
#in python come posso cercare il valore di un campo nella response di una chimata rest?
#auto-py-to-exe
#pyinstaller --onefile prova.py  //per generare .exe

#conda install -c anaconda pandas
import pandas as pd 
import requests
import json
import numpy as np
import time
import os
import getpass
import openpyxl as pyxl
import asyncio
#import aiohttp


def login():
    #url = 'https://idpint.coding.sum.testfactory.copergmps/sbopenamrest/api/oidcappservice'
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

def prova():
    #url = 'https://idpint.coding.sum.testfactory.copergmps/sbopenamrest/api/oidcappservice'
    url = 'https://digitaladvservices.mps.gmps.global/api/wv_da/v09/digitaladvisoryconsulenzafinanziaria/datiportafoglio/search'
    headers = {'Content-Type': 'application/json'} 
    headers = {'Accept':'application/json',
                'Content-Type':'Java-SDK',
                'Token':'$1WM2:{218BEA67-A9BF-44D4-B1D7-4EE8D4ACDBE7',
                'Cookie':'dtCookie=v_4_srv_1_sn_0B2A60C06FD092E5C6E1034542B75578_perc_100000_ol_0_mul_1_app-3Af4a0b5b296c13a14_1'
                }
    data = {
  "cdServizioChiamante": "Prometeia",
  "cdUtente": "S510987",
  "cdNDC": 118914507,
  "cdNGR": 0,
  "cdAbi": 1030,
  "tyRapportiCollegati": "0",
  "fgRefresh": 'false'
}
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    #jwt=response.text.split(':')[1]
    #print('JWT:' + jwt)
    return response.text

def loginAthena(jwt):
    #url = 'https://digitaladv-be.coding.mps.testfactory.copergmps/dashboard-rs/customers12/access/1030_16371718?lang=it'
    url = 'https://digitaladv-pfpbe.mps.gmps.global/pfp-rs/recommendations/1030_16371718?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_16371718'
    autorization = 'Bearer'+ jwt
    autorization = autorization.replace('"', '')
    autorization = autorization.replace('}', '')
    #print(autorization)
    headers = {'Content-Type': 'application/json','Authorization': autorization} 
    response = requests.get(url, headers=headers, verify=False)
    print(response.text)
    return response.text

def countNDCad1(jwt):
    url = 'https://digitaladv-pfpbe.coding.mps.testfactory.copergmps/pfp-rs/recommendations/1030_16371718?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_16371718'
    #url = 'https://digitaladv-pfpbe.coding.mps.testfactory.copergmps/pfp-rs/recommendations/1030_16371718?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_16371718'
    #url = 'https://digitaladv-pfpbe.mps.gmps.global/pfp-rs/recommendations/1030_16371718?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_16371718'
    autorization = 'Bearer'+ jwt
    autorization = autorization.replace('"', '')
    autorization = autorization.replace('}', '')
    #print(autorization)
    headers = {'Content-Type': 'application/json','Authorization': autorization} 
    #print (headers)
    #response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
    #null=None
    file_path = os.path.join(os.path.dirname(__file__), 'yac.json')
    file_path2 = os.path.join(os.path.dirname(__file__), 'out.json')

    with open(file_path, 'r') as file:
     json_data = json.load(file)
    
    #body_json = json.dumps(data, default=str)
    response = requests.put(url, json=json_data, headers=headers,verify=False)
    #print('INDICE: ' + response.text)
    #data2 = json.loads(response.text)
    #value = data2['count']
    #print('Numero NDC con Strategia ad 1 su INDICE: ' + str(value))
    with open(file_path2, 'w') as out_file:
        json.dump(response.json(), out_file)
    return response.text
    


user = os.environ.get("USERNAME")
print ("Utente: "+user)
passwd = getpass.getpass("Inserisci la tua password: ")

prova() 
jwt = login()
registrazione = loginAthena(jwt)
print (registrazione)
#countNDCad1SuIndice = countNDCad1(jwt)
#print (countNDCad1SuIndice)
#updateNDCstrategiaNULL()
