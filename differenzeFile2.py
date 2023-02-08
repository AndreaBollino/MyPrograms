from difflib import Differ
 
with open('V:\\batch\\catalogoTM.txt') as file_1, open('V:\\batch_gov\\catalogoTM.txt') as file_2:
    differ = Differ()
 
    for line in differ.compare(file_1.readlines(), file_2.readlines()):
        print(line)
