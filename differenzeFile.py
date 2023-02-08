# Importing difflib
import difflib
import pprint
import sys
import re
from sys import argv

def catalogo(file1,file2): 
    with open('V:\\batch\\'+file1) as file_1:
        file_1_text = file_1.readlines()
 
    with open('V:\\batch_gov\\'+file2) as file_2:
        file_2_text = file_2.readlines()

    diffFile = open('diffFile.txt', 'w')
    # Find and print the diff:
    for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile='V:\\batch\\'+file1,
            tofile='V:\\batch_gov\\'+file2, lineterm=''):
        #print(line)
        if line.startswith('+01030'):
            found = re.search(';(.+?);', line).group(1)
            #print(found+'\n')
            diffFile.write(found+'\n')
         #pprint.pformat(line)

    diffFile.close()
    #print('TITOLI MANCANTI su '+'  '+file1 )
    seen = set()
    with open('diffFile.txt') as infile:
        with open('output.txt', 'w') as outfile:
            for line in infile:
                if line not in seen:
                    outfile.write(line)
                    seen.add(line)
                    print(line+'\n')
                    #print(line)
    outfile.close()
if __name__=='__main__':
    catalogo('catalogoTM.txt','catalogoTM.txt')
    finito = input()
##    from sys import argv
##    if (len(argv) > 2):
##        print mcd(int(argv[1]), int(argv[2]))
##    else:
##        print 'Numero di argomenti insufficiente'
    
#sys.exit()


