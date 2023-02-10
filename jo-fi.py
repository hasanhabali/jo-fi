import subprocess
import re

def install_dependencies():
    subprocess.run("pip install re", shell=True, check=True)

def get_network_list():
    command = "sudo iwlist wlan0 scan | egrep 'ESSID|Address|Encryption key|Quality'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode("utf-8")

    # Split the output into separate networks
    networks = re.split("Cell [0-9][0-9] - ", out)[1:]

    # Parse information for each network
    network_list = []
    for network in networks:
        ssid = re.findall("ESSID:\"(.*)\"", network)[0]
        bssid = re.findall("Address: (.*)", network)[0]
        encryption = re.findall("Encryption key:(.*)", network)[0].strip()
        quality = re.findall("Quality=(.*)", network)[0].strip()
        
        network_list.append([ssid, bssid, encryption, quality])
        
    return network_list

def print_table(rows, headers=["SSID", "BSSID", "Encryption", "Quality"]):
    # Determine the max length of each column
    col_width = [max(len(str(x)) for x in col) for col in zip(*rows)]

    # Print headers
    print("\033[31mJO-WI SCANNER\033[0m")
    print("| " + " | ".join(str(x).ljust(col_width[i]) for i, x in enumerate(headers)) + " |")

    # Print separator
    print("|" + "|".join("-" * (width + 2) for width in col_width) + "|")

    # Print rows
    for row in rows:
        print("| " + " | ".join(str(x).ljust(col_width[i]) for i, x in enumerate(row)) + " |")

install_dependencies()
network_list = get_network_list()
print_table(network_list)
