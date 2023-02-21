#import the necessary libraries 
import os
import glob

#function to search for a string in files with .txt and .csv extension 
def search_string(string, directory): 
    #loop through all the files in the directory 
    for filename in glob.glob(os.path.join(directory, '*.txt')): 
        with open(filename) as f: 
            #loop through each line of the file 
            for line in f: 
                #check if the given string is present in the line 
                if string in line: 
                    print("Found string '{}' in file '{}' with comment: {}".format(string, filename, line))

    for filename in glob.glob(os.path.join(directory, '*.csv')): 
        with open(filename, encoding="ISO-8859-1") as f: 
             #open(filename, encoding="utf-8")
             #open(filename, errors="ignore")
            #loop through each line of the file 
            #aggiungi try exeption per UnicodeDecodeError e in caso di errore vai avanti con il for
            try:
             for line in f: 
                #check if the given string is present in the line  
                if string in line:  
                    print("Found string '{}' in file '{}' with comment: {}".format(string, filename, line))
            except:
                continue
                    												  

    	#get input from user - string to search and directory path  
string = input("Enter a string to search in batch_gov : ")  
#directory = input("Enter directory path : ")  
directory = 'V:\\batch_gov'

    #call function to search for a given string  
search_string(string, directory)
ciccio=input('Ricerca Finita in batch_gov inserisci qualcosa: ')
string2 = input("Enter a string to search in batch : ")  
search_string(string2, 'V:\\batch')
ciccio=input('Ricerca Finita in batch inserisci qualcosa: ')
