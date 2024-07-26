package main

import (
	"fmt"
	"net"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

func main() {

	fmt.Print("\n1. Network Information:\n")

	// Get list of network interfaces
	interfaces, err := net.Interfaces()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Iterate over each network interface
	for _, iface := range interfaces {
		fmt.Println("Interface Name:", iface.Name)
		fmt.Println("  Interface Hardware Address (MAC):", iface.HardwareAddr)

		// Get list of interface addresses
		addrs, err := iface.Addrs()
		if err != nil {
			fmt.Println("Error getting addresses for interface", iface.Name, ":", err)
			continue
		}

		// Iterate over each address
		for _, addr := range addrs {
			fmt.Println("  IP Address:", addr)
		}

		fmt.Println()
	}

	fmt.Println("\n----------------------------------")

	fmt.Print("\n2. Distro of OS: \n")
	// Execute the 'lsb_release' command to get distribution information
	cmd := exec.Command("lsb_release", "-a")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Convert output to string
	outputStr := string(output)

	// Split the output into lines
	lines1 := strings.Split(outputStr, "\n")

	// Parse and print distribution information
	for _, line := range lines1 {

		fmt.Println(line)
	}
	fmt.Println("\n----------------------------------")

	fmt.Print("\n3. Distro information:\n")

	fmt.Println("\n----------------------------------")

	fmt.Print("\n4. Installed software and packages: ")

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
		// fmt.Println(type(parts))
		if len(parts) > 0 {
			fmt.Println(parts[0])
		}

	}

	fmt.Println("\n----------------------------------")

	fmt.Print("\n5. Local System Information:\n")

	osName := runtime.GOOS

	// Get the architecture (32 or 64 bit)
	arch := runtime.GOARCH

	// Get the number of logical CPUs
	numCPU := runtime.NumCPU()

	// Get the hostname
	hostname, err := os.Hostname()
	if err != nil {
		fmt.Println("Error getting hostname:", err)
		return
	}

	// Print system information
	fmt.Println("Operating System:", osName)
	fmt.Println("Architecture:", arch)
	fmt.Println("Number of CPUs:", numCPU)
	fmt.Println("Hostname:", hostname)

}
