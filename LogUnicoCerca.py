import os
def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line[259:264] == '00000':
                outfile.write(line)

if __name__ == "__main__":
    input_path = r'C:\APPO\LOG\garanteprivacy.txt'
    #input_path = r'V:\batch_pfp\GARANTE\garanteprivacy_ieri.txt'
    #input_path = r'V:\batch_pfp\GARANTE\garanteprivacy.txt'
    output_path = r'C:\APPO\LOG\output.txt'
    process_file(input_path, output_path)
    #prova
    #prova2
