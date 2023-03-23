import os
import xml.etree.ElementTree as ET

# Path to the directory containing the XML files
directory = 'C:\\Users\\S511480\\Desktop\\Python_MieProgrammi\\MyPrograms\\xml\\'

# List of all XML files in the directory 
files = os.listdir(directory) 

for file in files: 

    # Parse each XML file 
    tree = ET.parse(directory + file) 

    # Get root element of each XML file  
    root = tree.getroot() 

    # Iterate over all elements in the root element  
    for element in root.iter():  

        # Check if element has attribute name and value 'PERIODO'  
        if 'name' in element.attrib and element.attrib['name'] == 'PERIODO':  

            # Print value of this element  
            print(element.text)
            element.text = 'II TRIMESTRE 2023'

            # Write back to the file by using write() method of ElementTree object    
            tree.write(directory + file, encoding="UTF-8", xml_declaration=True)
			
            ciccio = directory + file
            with open(ciccio, "r") as file:
                lines = file.readlines()

            lines[0] = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'

            with open(ciccio, "w") as file:
                file.writelines(lines)