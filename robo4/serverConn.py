import ctypes
import os
from ctypes import Structure, windll, WinError
from getpass import getpass

# Definisci la struttura NETRESOURCE
class NETRESOURCE(Structure):
    _fields_ = [
        ("dwScope", ctypes.c_ulong),
        ("dwType", ctypes.c_ulong),
        ("dwDisplayType", ctypes.c_ulong),
        ("dwUsage", ctypes.c_ulong),
        ("lpLocalName", ctypes.c_wchar_p),
        ("lpRemoteName", ctypes.c_wchar_p),
        ("lpComment", ctypes.c_wchar_p),
        ("lpProvider", ctypes.c_wchar_p),
    ]

# Carica la DLL di Windows
mpr = windll.mpr

# Definisci la funzione WNetAddConnection2
WNetAddConnection2 = mpr.WNetAddConnection2W
WNetAddConnection2.argtypes = [ctypes.POINTER(NETRESOURCE), ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_ulong]
WNetAddConnection2.restype = ctypes.c_ulong

# Impostazioni della connessione
remote_path = r"\\LX103005850532.mps.local\Logs"
username = "DO000005850001\S511480"
password = getpass("Inserisci la password: ")

# Crea un'istanza di NETRESOURCE
net_resource = NETRESOURCE()
net_resource.dwType = 1  # RESOURCETYPE_DISK
net_resource.lpRemoteName = remote_path

# Chiamata a WNetAddConnection2
result = WNetAddConnection2(ctypes.byref(net_resource), password, username, 0)

if result == 0:
    print("Connessione riuscita!")
    
    # Ottieni l'elenco dei file nella directory remota
    file_list = os.listdir(remote_path)
    
    print("Elenco dei file nella directory remota:")
    for file_name in file_list:
        print(file_name)
    # Chiudi la connessione quando hai finito
    mpr.WNetCancelConnection2W(remote_path, 0, True)

else:
    print(f"Errore durante la connessione: {result}, {WinError(result).strerror}")
