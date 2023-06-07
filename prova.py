""" def hello():
    print('Ueeee')

hello()


def getAnswer(number):
    if number == 1:
        return 'sicuro'

fortuna=getAnswer(1)
print(fortuna)
 """
# class Dog:
#     def __init__(self, name, breed):
#         self.name = name
#         self.breed = breed
#     def bark(self):
#         print("Woof!")

# my_dog = Dog("Fido", "Golden Retriever")
# print(my_dog.name) # "Fido"
# my_dog.bark() # "Woof!"

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_whee():
#     print("Whee!")

# say_whee()

# generator function
""" def my_gen():
    n = 1
    print('This is printed first')
    yield n

    n += 1
    print('This is printed second')
    yield n

    n += 1
    print('This is printed at last')
    yield n

# using for loop
for item in my_gen():
    print(item) """

# import threading
# import time

# def worker():
#     time.sleep(5)
#     print(str(threading.get_ident())+"\n")
#     #print(n)
#     #time.spleep(10/i)
#     #secondi=10/n
    

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#     t.start() 

# import threading

# def worker():
#     print(threading.get_ident())

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker)
#     #threads.append(t)
#     t.start()

# try:
#     x = 1 / 0
# except ZeroDivisionError as e:
#     print("Error Code:", e)

""" #scrivi uno shell script che prende qualsiasi carattere prima di .zip usando (.*?)
import re 

string = "dash-lx103000600333.testfactory.copergmps.2023-02-08.zip" 
match = re.search("(.*?)\.zip", string) 
if match: 
    print (match.group(1)) """
#scrivi print in java
#scrivi programma python che cerca una stringa su file .dat contenuto in file .zip
#scrivi programma python che cerca una stringa in un file .dat
# import zipfile 
# import os 

# #apri il file .zip 
# with zipfile.ZipFile('datafeed.zip', 'r') as zip_ref: 
#     #estrai tutti i file dall'archivio .zip 
#     zip_ref.extractall() 
    
# #cerca la stringa in tutti i file .dat estratti dall'archivio .zip 
# for filename in os.listdir(): 
#     if filename.endswith(".dat"): 
#         with open(filename, 'r', encoding="ISO-8859-1") as f: 
#             for line in f: 
#                 string = "IT0005537094"
#                 if string in line:
#                 #if "IT0005537094" in line: 
#                     print("La stringa è stata trovata nel file {}".format(filename))
#                     #print("Found string '{}' in file '{}' with comment: {}".format(string, filename, line))


#scrivi programma python che estrae i valori presenti nella colonna H di un file xls e questi valori non devono essere presenti nella colonna B di un altro foglio xls
""" import pandas as pd 

# lettura dei dati da file xls 
df1 = pd.read_excel('file_guida_sisco.xlsx') 
df2 = pd.read_excel('AthenaCommissioniPlatinum.xlsx') 

  
# estrazione dei valori dalla colonna H del primo file  
valori_H = df1['NDC_DEST'] 
pippo = valori_H.to_list()
  
# estrazione dei valori dalla colonna B del secondo file  
valori_B = df2['B'] 
ciccio = valori_B.to_list()

for elemento in ciccio: 
    if elemento not in pippo: 
        print(elemento) """
  
# confronto tra i due set di valori e estrazione dei valori presenti nella colonna H ma non nella colonna B  
#valori_H_non_in_B = [v for v in valori_H if v not in valori_B] 
  
# stampa dei risultati ottenuti  
#print(valori_H_non_in_B) 
#scrvi programma python che confronta 2 liste ed scrive solo gli elementi della prima lista che non sono nella seconda
#scrivi codice python che prende in input una lista di file xml contenuti in una directory e per ogni xml cerca elemento <field name="PERIODO"> sostituisce il testo con "ciccio" e poi aggiunge al file xml come prima riga ""
import os
import sys
import xml.etree.ElementTree as ET
from colorama import Fore
print(Fore.GREEN + "hello world")
print(Fore.GREEN + str(sys.path))

# Path to the directory containing the XML files
directory = 'C:\\Users\\S511480\\Desktop\\Python_MieProgrammi\\MyPrograms\\xml\\'

# List of all XML files in the directory 
files = os.listdir(directory) 

for file in files: 

    # Parse each XML file 
    tree = ET.parse(directory + file) 

    # Get root element of each XML file  
    root = tree.getroot() 

    # Iterate over all elements in the root element  
    for element in root.iter():  

        # Check if element has attribute name and value 'PERIODO'  
        if 'name' in element.attrib and element.attrib['name'] == 'PERIODO':  

            # Print value of this element  
            print(element.text)
            element.text = 'II TRIMESTRE 2023'

            # Write back to the file by using write() method of ElementTree object    
            tree.write(directory + file, encoding="UTF-8", xml_declaration=True)
			
            ciccio = directory + file
            with open(ciccio, "r") as file:
                lines = file.readlines()

            lines[0] = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'

            with open(ciccio, "w") as file:
                file.writelines(lines)

#scrivi programma python che sostituisce la prima riga di un file xml con la stringa "<?xml version="1.0" encoding="UTF-8" standalone="no"?>"
#python trova file maggiori di 100 MB ad eccezione della directory c:Windows e directory C:\Program Files quando li trovi scrivi file e dimensione
import os

for root, dirs, files in os.walk("/"):
    if root.startswith("C:/Windows"):
        continue
    for file in files:
        path = os.path.join(root, file)
        if os.path.getsize(path) > 100000000:
            print(path) 
#linux assegna ad una variabile istruzione "cat /tmp/hosts.old | grep localdomain4"


