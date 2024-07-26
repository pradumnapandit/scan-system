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

if __name__ == "__main__":
    # Get installed Packages from the system
    print("\nInstalled Packages as below:")
    while True:
        distro = input("Enter your Linux distribution (debian/centos): ").lower()

        if distro in ("debian", "centos"):
        
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