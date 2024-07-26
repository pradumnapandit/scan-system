import ipaddress

def find_network_range(ip, subnet_mask):
    # Create an IPv4Network object
    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
    
    # Get the network address and broadcast address
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    
    return network_address, broadcast_address


if __name__ == "__main__":
    # Find the network range
    ip = "192.168.1.10"
    subnet_mask = "255.255.255.0"
    network_address, broadcast_address = find_network_range(ip, subnet_mask)

    # Print the network range
    print(f"Network Address: {network_address}")
    print(f"Broadcast Address: {broadcast_address}")

