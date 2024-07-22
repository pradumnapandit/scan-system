import subprocess
import apt

def get_installed_software(distro):
  """
  Retrieves installed software and packages for the specified Linux distribution.

  Args:
      distro: String representing the distribution (e.g., "ubuntu", "centos").

  Returns:
      list: A list of software/package names (if successful).
  """

  if distro == "ubuntu":
    try:
      cache = apt.Cache()
      installed_packages = [pkg for pkg in cache if pkg.is_installed]
      return installed_packages
      # Use dpkg for Debian-based systems
      #output = subprocess.run(["dpkg-query", "-l"], capture_output=True, text=True, check=True)
      #packages = output.stdout.strip().split("\n")[0:]  # Remove header and split lines
      #return [package.split()[0] for package in packages]  # Extract package names
    except subprocess.CalledProcessError:
      print("Failed to retrieve software list using dpkg.")
      return []

  elif distro == "centos":
    try:
      # Use rpm for RPM-based systems
      output = subprocess.run(["rpm", "-qa"], capture_output=True, text=True, check=True)
      packages = output.stdout.strip().split("\n")
      return packages
    except subprocess.CalledProcessError:
      print("Failed to retrieve software list using rpm.")
      return []

  else:
    print(f"Unsupported distribution: {distro}")
    return []

def main():
  """
  Prompts for the Linux distribution and displays installed software/packages.
  """

  while True:
    distro = input("Enter your Linux distribution (ubuntu/centos): ").lower()
    if distro in ("ubuntu", "centos"):
      installed_software = get_installed_software(distro)
      if installed_software:
        print("Installed software and packages:")
        for item in installed_software:
          print(item)
      else:
        print("No software found.")
      break
    else:
      print("Invalid distribution. Please try again.")

if __name__ == "__main__":
  main()