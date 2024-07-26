package main

import (
  "fmt"
  "os/exec"
  "strings"
)

func getInstalledSoftware(distro string) ([]string, error) {
  var cmd *exec.Cmd
  if distro == "ubuntu" {
    //cmd = exec.Command("dpkg-query", "-l")
    out, err := exec.Command("dpkg", "--get-selections").Output()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Split the output by newline and extract package names
	lines := strings.Split(string(out), "\n")
	fmt.Println("Installed packages:")
	for _, line := range lines {
		parts := strings.Fields(line)
		if len(parts) > 0 {
			fmt.Println(parts[0])
		}
	}
  } else if distro == "centos" {
    cmd = exec.Command("rpm", "-qa")
  } else {
    return nil, fmt.Errorf("unsupported distribution: %s", distro)
  }

  out, err := cmd.Output()
  if err != nil {
    return nil, fmt.Errorf("failed to run command: %w", err)
  }

  // Remove header line and split remaining lines by newline
  lines := strings.Split(strings.TrimSpace(string(out)), "\n")[1:]
  packages := make([]string, 0, len(lines))
  for _, line := range lines {
    // Extract package name (assuming first element)
    packages = append(packages, strings.Split(line, " ")[0])
  }

  return packages, nil
}

func main() {
  distro := "ubuntu" // Change to "centos" for CentOS

  installedSoftware, err := getInstalledSoftware(distro)
  if err != nil {
    fmt.Println(err)
    return
  }

  if len(installedSoftware) > 0 {
    fmt.Println("Installed software and packages:")
    for _, pkg := range installedSoftware {
      fmt.Println(pkg)
    }
  } else {
    fmt.Println("No software found.")
  }
}

