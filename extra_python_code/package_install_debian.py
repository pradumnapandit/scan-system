import apt

def get_installed_packages():
    cache = apt.Cache()
    installed_packages = [pkg for pkg in cache if pkg.is_installed]
    return installed_packages

if __name__ == "__main__":
    installed_packages = get_installed_packages()
    
    print("Installed packages:")
    for package in installed_packages:
        print(package.name)
