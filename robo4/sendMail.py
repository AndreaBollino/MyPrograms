import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Richiedi all'utente di inserire il proprio indirizzo email e la password in modo sicuro
email_address = input("Inserisci il tuo indirizzo email: ")
password = getpass.getpass("Inserisci la tua password: ")

# Creazione di un oggetto messaggio
msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = "bollino.andrea@gmail.com"  # Inserisci l'indirizzo email del destinatario
msg['Subject'] = "Oggetto della mail"

# Aggiungi il corpo del messaggio
body = "Questo è il testo del messaggio."
msg.attach(MIMEText(body, 'plain'))

# Connetti al server SMTP di Gmail
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, password)

    # Invia il messaggio
    text = msg.as_string()
    server.sendmail(email_address, "bollino.andrea@gmail.com", text)
    print("Messaggio inviato con successo!")

except Exception as e:
    print(f"Errore durante l'invio del messaggio: {str(e)}")

finally:
    # Chiudi la connessione al server SMTP
    server.quit()
