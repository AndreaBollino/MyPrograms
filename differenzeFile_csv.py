# Importing difflib
import difflib
import pprint
import sys
import re
from sys import argv

def catalogoCSV(file1,file2): 
    with open('V:\\batch\\'+file1) as file_1:
    #with open(file1) as file_1:
        file_1_text = file_1.readlines()
        
    with open('V:\\batch_gov\\'+file2) as file_2:
    #with open(file2) as file_2:
        file_2_text = file_2.readlines()

    diffFile2 = open('diffFile2.txt', 'w')
    # Find and print the diff:
    for line in difflib.unified_diff(
                file_1_text, file_2_text, fromfile='V:\\batch\\'+file1,
                #file_1_text, file_2_text, fromfile=file1,
            tofile='V:\\batch_gov\\'+file2, lineterm=''):
            #tofile=file2, lineterm=''):
        #print(line)
        #if (line.startswith('+') & ( not line.startswith('+++ V:\batch_gov\Anagrafica_Governance.csv'))):
        if (line.startswith('+') & (line.find('Anagrafica_Governance.csv') == -1)):
            #print(line+'\n')
            found = re.search(';(.+?);', line).group(1)
            #print(found)
            diffFile2.write(found+'\n')
##            #pprint.pformat(line)

    diffFile2.close()
    seen = set()
    with open('diffFile2.txt') as infile:
        with open('output2.txt', 'w') as outfile2:
            for line in infile:
                if line not in seen:
                    outfile2.write(line)
                    seen.add(line)
                    print(line)
    outfile2.close()
if __name__=='__main__':
    catalogoCSV('Anagrafica_Governance.csv','Anagrafica_Governance.csv')
    finito = input()
##    from sys import argv
##    if (len(argv) > 2):
##        print mcd(int(argv[1]), int(argv[2]))
##    else:
##        print 'Numero di argomenti insufficiente'
#finito = input()
#sys.exit()


