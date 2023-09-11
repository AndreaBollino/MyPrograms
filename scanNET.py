import nmap
nm = nmap.PortScanner()
results = nm.scan('192.168.1.0/24', '1-1024')
for host in results['scan']:
    print(f'{host}: {results["scan"][host]["tcp"].keys()}')