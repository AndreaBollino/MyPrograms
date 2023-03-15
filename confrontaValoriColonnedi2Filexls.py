import pandas as pd 

# lettura dei dati da file xls 
df1 = pd.read_excel('file_guida_sisco.xlsx') 
df2 = pd.read_excel('AthenaCommissioniPlatinum.xlsx') 
  
# estrazione dei valori dalla colonna H del primo file  
valori_H = df1['NDC_DEST'] 
pippo = valori_H.to_list()
  
# estrazione dei valori dalla colonna B del secondo file  
valori_B = df2['B'] 
ciccio = valori_B.to_list()
cicciotto = []
i=0
for elemento in ciccio: 
    if elemento not in pippo: 
        cicciotto.append(elemento)
        #print(elemento)
        i=i+1


print(cicciotto)
print(str(i))
corrispondenti_valori = df2[df2['B'].isin(cicciotto)]['F']
print(str(corrispondenti_valori.to_list()))
#scrivo programma python usando pandas che cerca i valori di una lista in una colonna di un foglio xls e estrae i corrispondenti valori di una altra colonna 
#python scrivi ciclo for che aggiunge valori ad una lista