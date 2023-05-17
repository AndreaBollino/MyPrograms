import csv

def filtro_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as file_in, open(output_file, 'w', newline='') as file_out:
        reader = csv.reader(file_in, delimiter=';')
        writer = csv.writer(file_out, delimiter=';')
        pippo=0

        for row in reader:
            if len(row) >= 6 and row[5] != "000000000000000,000":
                writer.writerow(row)
                pippo=pippo+1

        print("numero righe tenute " + str(pippo))

# Esempio di utilizzo
input_filename = "AthenaCommissioniPlatinum.csv"
output_filename = "AthenaCommissioniPlatinum_mod.csv"

filtro_csv(input_filename, output_filename)
print("Le righe sono state filtrate correttamente.")
