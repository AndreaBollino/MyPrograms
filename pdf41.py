import os

# Leggi il valore dal file indici.txt
def leggi_valori_da_file(file_path):
    with open(file_path, 'r') as file:
        valori = set(line.strip() for line in file)
    return valori

valori_file_path = 'indici41.txt'
valori_da_trovare = leggi_valori_da_file(valori_file_path)


# Percorso alla directory di origine
directory_origine = r"U:\1030\JForm\OutJform\00000"

# Percorso alla directory di destinazione
directory_destinazione = "41"

# Cerca i file che contengono il valore nel loro nome
for filename in os.listdir(directory_origine):
    #if valori_da_trovare in filename:
    for valore in valori_da_trovare:
                if valore in filename:
        # Costruisci i percorsi completi per i file di origine e destinazione
                    percorso_file_origine = os.path.join(directory_origine, filename)
                    percorso_file_destinazione = os.path.join(directory_destinazione, filename)
        
        # Copia il file nella directory di destinazione
                    with open(percorso_file_origine, "rb") as file_origine, open(percorso_file_destinazione, "wb") as file_destinazione:
                        file_destinazione.write(file_origine.read())
        
                    print(f"Copiato il file {filename} nella directory di destinazione.")
