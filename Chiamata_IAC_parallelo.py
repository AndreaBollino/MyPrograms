import asyncio
from random import random
from time import perf_counter
import aiohttp
import requests
import json
import os
import getpass
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

    #print (headers)
    #response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
    #null=None
file_path = os.path.join(os.path.dirname(__file__), 'yac.json')
file_path2 = os.path.join(os.path.dirname(__file__), 'out.json')

with open(file_path, 'r') as file:
    json_data = json.load(file)
    

url = "https://digitaladv.coding.mps.testfactory.copergmps/pfp-gui/index.html?DEST=scheda-cliente-plus&NDC=1030_6298409&PF=GA"

webbrowser.open(url)

user = os.environ.get("USERNAME")
print ("Utente: "+user)
passwd = getpass.getpass("Inserisci la tua password: ")

jwt = login()

autorization = 'Bearer'+ jwt
autorization = autorization.replace('"', '')
autorization = autorization.replace('}', '')
    #print(autorization)
headers = {'Content-Type': 'application/json','Authorization': autorization} 

#https://jackskylord.medium.com/python-aiohttp-and-asyncio-a0e55b18f77a
semaphore = asyncio.Semaphore(2)
async def make_request(async_session: aiohttp.ClientSession, url: str):
    # Semaphore for limiting concurrent requests to 10
    async with semaphore:
        # Asynchronous GET request
        async with async_session.put(url, json=json_data, headers=headers) as response:
        #/dashboard-rs/family/1030_6298409?areaTematica=ANAG
        #async with async_session.get(url, headers=headers) as response:
            # await a random sleep to avoid overloading the serve  
            
            #print("---Starting inter ---")
            
            

            #start_time_inter = perf_counter()
            
            #await asyncio.sleep(10)  
            
            await asyncio.sleep(random())       
            #print(perf_counter())
            #content = await response.json()
            
            if "241" in url:
                print("335 ", flush=True, sep="", end="")
            elif "digitaladv-be" in url:
                print("INIZ ", flush=True, sep="", end="")
            else: 
                print("329 ", flush=True, sep="", end="")
            #print (url+" ")
            #await asyncio.sleep(5)
            #await asyncio.sleep(random())     
            
            #end_time_inter = perf_counter()
            #total_time_inter = end_time_inter - start_time_inter
            #print(f"\n---Finished _inter in: {total_time_inter:.2f} seconds---")
            
            #with open(file_path2, 'w') as out_file:
               # json.dump(content, out_file)
                
            #print(content)
            #await asyncio.sleep(random())
            
            
async def makes_all_requests(urls: list[str]):
    # Store all tasks that will later be used with `asyncio.gather`
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as async_session:
        tasks = []
        for url in urls:
            # Create an asyncio.Task that will return a future
            task = asyncio.create_task(
                coro=make_request(
                    async_session=async_session,
                    url=url,
                )
            )
            tasks.append(task)

        # Run tasks using asyncio.gather
        await asyncio.gather(*tasks, return_exceptions=False)
#10.242.210.241   335
#10.242.210.243   329
#digitaladv-pfpbe.coding.mps.testfactory.copergmps

if __name__ == "__main__":
    
    urls1 = [
       'https://digitaladv-be.coding.mps.testfactory.copergmps/dashboard-rs/family/1030_6298409?areaTematica=ANAG',
       ] * 6
    urls2 = [
       'https://10.242.210.243:443/pfp-rs/recommendations/1030_6298409?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_6298409',
       'https://10.242.210.241:443/pfp-rs/recommendations/1030_6298409?lang=it&clearNotCheckedLines=true&suitabilityCheck=true&presenterCode=1030_6298409',
       ] * 15
    
    urls = urls1 + urls2
    
    """ urls = [
       'https://digitaladv-be.coding.mps.testfactory.copergmps/dashboard-rs/family/1030_6298409?areaTematica=ANAG',
] * 30 """

    print("---Starting---")

    start_time = perf_counter()

    asyncio.run(makes_all_requests(urls=urls))

    end_time = perf_counter()
    total_time = end_time - start_time
    print(f"\n---Finished in: {total_time:.2f} seconds---")
