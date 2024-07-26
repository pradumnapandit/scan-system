import nmap
import psutil
import platform
import socket
import subprocess
import apt
import distro
import ipaddress
import fcntl
import struct

def scan_network(network_range):
    nm = nmap.PortScanner()
    print(f"Scanning network range: {network_range}")
    nm.scan(hosts=network_range, arguments='-sP')
    active_hosts = [(host, nm[host]['status']['state']) for host in nm.all_hosts()]
    return active_hosts

# def scan_host(host):
    nm = nmap.PortScanner()
    print(f"Scanning host: {host}")
    nm.scan(hosts=host, arguments='-sV')
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

def get_local_system_info():
    system_info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'cpu_count': psutil.cpu_count(),
        'memory': psutil.virtual_memory().total,
        'disk_partitions': []
    }
    for partition in psutil.disk_partitions():
        partition_info = {
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'fstype': partition.fstype,
            'total_size': psutil.disk_usage(partition.mountpoint).total
        }
        system_info['disk_partitions'].append(partition_info)
    return system_info

def get_running_processes():
    print("\nEntering into processes world")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            proc_info = proc.info
            proc_info['status'] = proc.status()
            proc_info['cpu_usage'] = proc.cpu_percent(interval=0.1)
            proc_info['memory_usage'] = proc.memory_info().rss
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def distro_info():
    distro_information=distro.id()
    return distro_information

def get_installed_software(distro):
  """
  Retrieves installed software and packages for the specified Linux distribution.

  Args:
      distro: String representing the distribution (e.g., "debian", "centos").

  Returns:
      list: A list of software/package names (if successful).
  """

  if distro == "debian":
    try:
      cache = apt.Cache()
      installed_packages = [pkg for pkg in cache if pkg.is_installed]
    #   installed_packages_string = ', '.join(installed_packages)
      return installed_packages

    except subprocess.CalledProcessError:
      print("Failed to retrieve software list using dpkg.")
      return []

  elif distro == "centos":
    try:
      # Use rpm for RPM-based systems
      output = subprocess.run(["rpm", "-qa"], capture_output=True, text=True, check=True)
      packages = output.stdout.stri
      p().split("\n")
      return packages
    except subprocess.CalledProcessError:
      print("Failed to retrieve software list using rpm.")
      return []

  else:
    print(f"Unsupported distribution: {distro}")
    return []

def get_linux_distribution():
    return distro.info("id")


def find_network_range(ip, subnet_mask):
    # Create an IPv4Network object
    network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
    
    # Get the network address and broadcast address
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    
    return network_address, broadcast_address

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname.encode('utf-8')[:15])
    )[20:24])

def get_network_info():
    interfaces = socket.if_nameindex()
    for ifindex, ifname in interfaces:
        try:
            ip_address = get_ip_address(ifname)
            hw_address = ':'.join(['{:02x}'.format((int(byte))) for byte in fcntl.ioctl(socket.socket(socket.AF_INET, socket.SOCK_DGRAM), 0x8927, struct.pack('256s', ifname.encode('utf-8')[:15]))[18:24]])
            print("Interface Name:", ifname)
            print("  IP Address:", ip_address)
            print("  Hardware Address (MAC):", hw_address)
            print()
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    # Scan the local network
    # ip = "192.168.1.10"
    # subnet_mask = "255.255.255.0"
    # network_address, broadcast_address = find_network_range(ip, subnet_mask)

    # # Print the network range
    # print("1. Network Information:")
    # print(f"Network Address: {network_address}")
    # print(f"Broadcast Address: {broadcast_address}")
    
    print("1. Network Information:")
    get_network_info()
   

    print("\n---------------------")

    print("\n2. Distro of OS:")
    distribution_info = get_linux_distribution()
    print(distribution_info)

    print("\n---------------------")
    # print("\nActive hosts:")
    # for host, status in network_address:
    #     print(f"Host: {host}, Status: {status}")
    #     if status == 'up':
    #         host_details = scan_host(host)
    #         print(f"\nDetails for host {host}:")
    #         print(host_details)

    # Get Distro Info
    print("\n3. Distro information:")
    distro_i = distro_info()
    print(distro_i)

    print("\n---------------------")
    # Get installed Packages from the system
    #print("\nInstalled Packages as below:")
    installed_software = get_installed_software(distro_i)
    if installed_software:
        print("\n4. Installed software and packages:")
        single_line_string = ', '.join(str(item) for item in installed_software)
        print(single_line_string)
        # for item in installed_software:
        #     print(item)
    else:
        print("No software found.")      

    print("\n---------------------")

    # Get local system information
    local_system_info = get_local_system_info()
    print("\n5. Local System Information:")
    print(local_system_info)


    # # Get running processes
    # running_processes = get_running_processes()
    # print("\nRunning Processes:")
    # for proc in running_processes:
    #     print(proc)
