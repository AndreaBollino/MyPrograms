# filecmp_dircmp_report.py
#https://robyp.x10host.com/3/filecmp.html
# pip3.11 install PySide
# C:\Users\S511480\AppData\Local\Programs\Python\Python311\Scripts\pip3.11

# Determina gli elementi che esistono in entrambe le directory
import filecmp
import os
from differenzeFile import catalogo
from differenzeFile_csv import catalogoCSV
#import differenzeFile_csv 

d1_contents = set(os.listdir('V:\\batch'))
d2_contents = set(os.listdir('V:\\batch_gov'))
common = list(d1_contents & d2_contents)
common.remove('datafeed.zip')
print('Ho escluso: datafeed.zip')

common_files = [
    f
    for f in common
    if os.path.isfile(os.path.join('V:\\batch_gov', f))
]
print('File comuni:', common_files)

# Confronta le directory
match, mismatch, errors = filecmp.cmpfiles(
    'V:\\batch',
    'V:\\batch_gov',
    common_files,
    shallow=False
)
print('CORRISPONDENZE        :', match)
print('MANCATE CORRISPONDENZE:', mismatch)
print('Errori                :', errors)
ciao=input()
for item in mismatch:
        if item == 'catalogoTM.txt' :
         print('TITOLI MANCANTI su '+'  '+item )
         catalogo(item,item)
         print('Confronto finito')
         pippo = input('Vai AVANTI scrivi qualcosa: ')	
        if item == 'Anagrafica_Governance.csv' :
         print('TITOLI MANCANTI su '+'  '+item )
         catalogoCSV(item,item)
         print('Confronto finito')
         ciccio = input('Vai AVANTI scrivi qualcosa: ')	
#finito = input()
