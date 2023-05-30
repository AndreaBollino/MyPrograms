# programma python che cancella file da un adirectory leggendo da un file txt stringa che compne il nome del file da cancellare 
import os 

# open the file with the list of files to delete 
with open('files_to_delete.txt', 'r') as f: 
    # read each line of the file 
    for line in f: 
        # get the filename from the line 
        filename = line.strip() 

        # check if the file exists in the directory 
        if os.path.exists(filename): 
            # delete the file if it exists 
            os.remove(filename)