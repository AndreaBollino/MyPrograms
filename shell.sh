# scrivi un bah script per cercare e sostituire una stringa in un file



#!/bin/bash

# This script will search and replace a string in a file

# Ask the user for the file name
echo -n "Enter the file name: "
read FILE_NAME

# Ask the user for the string to search for 
echo -n "Enter the string to search for: " 
read SEARCH_STRING 

# Ask the user for the string to replace with 
echo -n "Enter the string to replace with: " 
read REPLACE_STRING 

 # Search and replace using sed command 
 sed -i 's/$SEARCH_STRING/$REPLACE_STRING/g' $FILE_NAME