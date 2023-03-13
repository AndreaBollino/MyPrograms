import zipfile 
import os 
import shutil 


src_dir = 'V:\\batch_gov'
dst_dir = 'C:\\Users\\S511480\\Desktop\\Python_MieProgrammi\\MyPrograms'

for filename in os.listdir(src_dir): 
    if filename.endswith(".zip"): 
        shutil.copy(os.path.join(src_dir, filename), dst_dir)
#programma python che copia file da directory in directory locale
string = input("Scrivi ISIN da trovare in datafeed.zip  di Prometeia:  ") 
#apri il file .zip 
with zipfile.ZipFile('datafeed.zip', 'r') as zip_ref: 
    #estrai tutti i file dall'archivio .zip 
    zip_ref.extractall() 
    
#cerca la stringa in tutti i file .dat estratti dall'archivio .zip 
for filename in os.listdir(): 
    if filename.endswith(".dat"): 
        with open(filename, 'r', encoding="ISO-8859-1") as f: 
            for line in f: 
                #string = "IT0005537094"
                if string in line:
                #if "IT0005537094" in line: 
                    print("La stringa è stata trovata nel file {}".format(filename))
                    #print("Found string '{}' in file '{}' with comment: {}".format(string, filename, line))