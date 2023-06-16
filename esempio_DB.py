import cx_Oracle
import os

un = os.environ.get('USER_NAME')
pw = os.environ.get('PASSWORD')

cx_Oracle.init_oracle_client(config_dir="C:\\oracle\\ora12R2CL_32\\network\\admin")
connection = cx_Oracle.connect(user=un, password=pw, dsn="OraWV_NPWAADVISORYAPP_PROD.world", encoding="UTF-8")
#connection = cx_Oracle.connect("APTWGNPF", "BG7LB2QPVLNEIZPT", dsn="OraWV_NPWAADVISORYAPP_CODF.world", encoding="UTF-8")

cursor = connection.cursor()
query = "select * from NPWAPFP.tbl_guida_staging"
cursor.execute(query)

# Lettura dei risultati
for row in cursor:
    print(row)

# Chiusura della connessione
cursor.close()
connection.close()
