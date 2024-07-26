import nmap

def scan_network(network_range):
    # Create an nmap object
    nm = nmap.PortScanner()
    
    # Perform the scan
    print(f"Scanning network range: {network_range}")
    nm.scan(hosts=network_range, arguments='-sP')
    
    # Collect results
    active_hosts = [(host, nm[host]['status']['state']) for host in nm.all_hosts()]
    
    return active_hosts

def scan_host(host):
    # Create an nmap object
    nm = nmap.PortScanner()
    
    # Perform the scan
    print(f"Scanning host: {host}")
    nm.scan(hosts=host, arguments='-sV')
    
    # Collect results
    host_info = {
        'host': host,
        'state': nm[host].state(),
        'protocols': []
    }
    
    for proto in nm[host].all_protocols():
        ports = nm[host][proto].keys()
        protocol_info = {
            'protocol': proto,
            'ports': []
        }
        for port in ports:
            port_info = {
                'port': port,
                'state': nm[host][proto][port]['state'],
                'name': nm[host][proto][port]['name'],
                'product': nm[host][proto][port]['product'],
                'version': nm[host][proto][port]['version'],
                'extrainfo': nm[host][proto][port]['extrainfo'],
            }
            protocol_info['ports'].append(port_info)
        host_info['protocols'].append(protocol_info)
    
    return host_info

if __name__ == "__main__":
    network_range = input("Enter the network range to scan (e.g., 192.168.1.0/24): ")
    active_hosts = scan_network(network_range)
    
    print("\nActive hosts:")
    for host, status in active_hosts:
        print(f"Host: {host}, Status: {status}")
        
        if status == 'up':
            host_details = scan_host(host)
            print(f"\nDetails for host {host}:")
            print(host_details)

