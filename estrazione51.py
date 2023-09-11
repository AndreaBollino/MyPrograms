import csv
def leggi_valori_da_file(file_path):
    with open(file_path, 'r') as file:
        valori = set(line.strip() for line in file)
    return valori

def estrai_righe_da_file(input_file_path, output_file_path, valori_da_trovare):
    #filtered_rows = []
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            if any(valore in line for valore in valori_da_trovare):
                output_file.write(line)

def ordina_file_per_ottavo_elemento(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        #header = next(reader)
        sorted_rows = sorted(reader, key=lambda row: int(row[7]))  # Ordina per ottavo elemento (indice 7)
        print(sorted_rows)
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        #writer.writerow(header)
        writer.writerows(sorted_rows)

def main():
    # Percorso del file contenente i valori da cercare
    valori_file_path = 'indici.txt'
    valori_da_trovare = leggi_valori_da_file(valori_file_path)

    # Percorsi dei file di input e output
    input_file_path = 'file_guida_sisco.csv'
    output_file_path = 'file_guida_sisco_new.csv'

    # Estrai le righe dal file di input e scrivile nel nuovo file
    estrai_righe_da_file(input_file_path, output_file_path, valori_da_trovare)
    ordina_file_per_ottavo_elemento("file_guida_sisco_new.csv")
    with open('file_guida_sisco.csv', 'r') as file_guida_originale:
        prima_riga = next(file_guida_originale)
        with open('file_guida_sisco_new.csv', 'r+') as file_guida_nuovo:
            contenuto = file_guida_nuovo.read()
            file_guida_nuovo.seek(0, 0)
            file_guida_nuovo.write(prima_riga.rstrip('\r\n') + '\n' + contenuto)
    
    #ordina_file_per_ottava_colonna("file_guida_sisco_new.csv")
    #ottavi_elementi = estrai_ottavo_elemento('file_guida_sisco_new.csv')
    #print(ottavi_elementi)

if __name__ == "__main__":
    main()
