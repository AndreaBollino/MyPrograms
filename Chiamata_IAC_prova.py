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
import aiohttp

from time import perf_counter

import webbrowser

def login():
    url = 'https://idpint.coding.sum.testfactory.copergmps/sbopenamrest/api/oidcappservice'
    #url = 'https://idpint.sum.gmps.global/sbopenamrest/api/oidcappservice'
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

def loginAthena(jwt):
    #url = 'https://digitaladv-be.coding.mps.testfactory.copergmps/dashboard-rs/customers12/access/1030_16371718?lang=it'
    url = 'https://digitaladv-be.coding.mps.testfactory.copergmps/dashboard-rs/login'
    #url = 'https://digitaladv-pfpbe.mps.gmps.global/pfp-rs/recommendations/1030_16371718?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_16371718'
    autorization = 'Bearer'+ jwt
    autorization = autorization.replace('"', '')
    autorization = autorization.replace('}', '')
    #print(autorization)
    headers = {'Content-Type': 'application/json','Authorization': autorization} 
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def suitabilityCheck(jwt,url):
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
    start_time_inter = perf_counter()
            #await asyncio.sleep(10)  
            #await asyncio.sleep(random())       
    #response = requests.put(url, json=json_data, headers=headers,verify=False)
    requests.put(url, json=json_data, headers=headers,verify=False)
            
    end_time_inter = perf_counter()
    total_time_inter = end_time_inter - start_time_inter
    print(f"\n---Finished _inter in: {total_time_inter:.2f} seconds---")
    
    #print('INDICE: ' + response.text)
    #data2 = json.loads(response.text)
    #value = data2['count']
    #print('Numero NDC con Strategia ad 1 su INDICE: ' + str(value))
    
    #with open(file_path2, 'w') as out_file:
     #   json.dump(response.json(), out_file)
        
    #print(response.text)
    #return response.text
    
    

url = "https://digitaladv.coding.mps.testfactory.copergmps/pfp-gui/index.html?DEST=scheda-cliente-plus&NDC=1030_6298409&PF=GA"
webbrowser.open(url)

user = os.environ.get("USERNAME")
print ("Utente: "+user)
passwd = getpass.getpass("Inserisci la tua password: ")

jwt = login()

def makes_all_requests(urls: list[str]):
    for url in urls:
        suitabilityCheck(jwt,url)


if __name__ == "__main__":
    urls = [
    'https://digitaladv-pfpbe.coding.mps.testfactory.copergmps/pfp-rs/recommendations/1030_6298409?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_6298409',
    ] * 10

    print("---Starting---")

    start_time = perf_counter()

    makes_all_requests(urls=urls)

    end_time = perf_counter()
    total_time = end_time - start_time
    print(f"\n---Finished in: {total_time:02f} seconds---")
    



""" 6298409
222620198
225726538
1695957
11337502
15920342
45680797
6209953
7064975 """

#registrazione = loginAthena(jwt)
#print (registrazione)

#suitabilityCheckout = suitabilityCheck(jwt)
#print (suitabilityCheckout)

#updateNDCstrategiaNULL()
