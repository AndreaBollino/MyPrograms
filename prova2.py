import os
import xml.etree.ElementTree as ET

# Percorso della cartella contenente i file XML
directory = 'C:\\Users\\S511480\\Desktop\\Python_MieProgrammi\\MyPrograms\\xml\\'

# Testo da sostituire al campo "PERIODO"
replacement_text = 'II TRIMESTRE 2023'

# Iterazione su tutti i file XML nella cartella
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        fullname = os.path.join(directory, filename)
        
        # Parsing del file XML
        tree = ET.parse(fullname)
        root = tree.getroot()
        
        # Sostituzione del testo nel campo "PERIODO"
        for field in root.iter("field"):
            if field.get("name") == "PERIODO":
                field.text = replacement_text
        
        # Aggiunta dell'intestazione XML
        declaration = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        root.insert(0, ET.fromstring(declaration))
        
        # Scrittura del file XML aggiornato
        tree.write(fullname, encoding="UTF-8", xml_declaration=False)