#!/usr/bin/env python3
import subprocess
import psutil
from colorama import Fore, Style
import sys

# Function to find active network cards
def find_active_network_cards():
    active_interfaces = []
    network_interfaces = psutil.net_if_stats()
    for interface, stats in network_interfaces.items():
        if stats.isup:
            active_interfaces.append(interface)
    return active_interfaces

# Function to set DNS
def set_dns(network_card, dns_server1, dns_server2):
    try:
        dns_servers_str = f"{dns_server1} {dns_server2}".strip()
        if not dns_servers_str:
            print(Fore.RED + "No DNS server IP addresses provided. Cannot set DNS." + Style.RESET_ALL)
            return

        # Get the name of the active connection for the selected network card
        get_con_name_cmd = f"nmcli -t -f NAME,DEVICE connection show --active | grep -Fw '{network_card}' | head -n 1 | cut -d: -f1"
        connection_name = subprocess.check_output(get_con_name_cmd, shell=True, text=True, stderr=subprocess.PIPE).strip()

        if not connection_name:
            print(Fore.RED + f"Could not find an active connection for network card '{network_card}'." + Style.RESET_ALL)
            print(Fore.YELLOW_EX + "Please ensure the network card is active and has an established connection." + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + f"Attempting to set DNS for connection '{connection_name}' on device '{network_card}' to: {dns_servers_str}" + Style.RESET_ALL)

        # Modify DNS servers
        set_dns_cmd = f"sudo nmcli connection modify '{connection_name}' ipv4.dns '{dns_servers_str}'"
        subprocess.run(set_dns_cmd, shell=True, check=True, text=True, capture_output=True)

        # Ignore DNS from DHCP
        ignore_auto_dns_cmd = f"sudo nmcli connection modify '{connection_name}' ipv4.ignore-auto-dns yes"
        subprocess.run(ignore_auto_dns_cmd, shell=True, check=True, text=True, capture_output=True)
        
        print(Fore.CYAN + f"Applying changes to connection '{connection_name}'..." + Style.RESET_ALL)
        apply_cmd = f"sudo nmcli connection up '{connection_name}'"
        result = subprocess.run(apply_cmd, shell=True, check=True, text=True, capture_output=True)
        if result.stdout and "successfully activated" in result.stdout:
            print(Fore.CYAN + result.stdout.strip() + Style.RESET_ALL)
        elif result.stderr: # Print stderr if apply_cmd had non-fatal issues but didn't fail check=True
            print(Fore.YELLOW_EX + result.stderr.strip() + Style.RESET_ALL)

        print(Fore.LIGHTGREEN_EX + "DNS servers set successfully." + Style.RESET_ALL)
        print(Fore.YELLOW_EX + "You might need to restart your browser or application to use the new DNS settings." + Style.RESET_ALL)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error executing command: {e.cmd}" + Style.RESET_ALL)
        error_output = ""
        if e.stdout:
            error_output += f"Stdout: {e.stdout.strip()}\\n"
        if e.stderr:
            error_output += f"Stderr: {e.stderr.strip()}"
        if error_output:
            print(Fore.RED + error_output + Style.RESET_ALL)
        print(Fore.RED + "Failed to set DNS." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred while setting DNS: {e}" + Style.RESET_ALL)

# Function to reset DNS
def reset_dns(network_card):
    try:
        # Get the name of the active connection for the selected network card
        get_con_name_cmd = f"nmcli -t -f NAME,DEVICE connection show --active | grep -Fw '{network_card}' | head -n 1 | cut -d: -f1"
        connection_name = subprocess.check_output(get_con_name_cmd, shell=True, text=True, stderr=subprocess.PIPE).strip()

        if not connection_name:
            print(Fore.RED + f"Could not find an active connection for network card '{network_card}'." + Style.RESET_ALL)
            print(Fore.YELLOW_EX + "Please ensure the network card is active and has an established connection." + Style.RESET_ALL)
            return

        print(Fore.CYAN + f"Attempting to reset DNS for connection '{connection_name}' on device '{network_card}'..." + Style.RESET_ALL)

        # Clear manually set DNS servers
        reset_dns_cmd = f"sudo nmcli connection modify '{connection_name}' ipv4.dns ''"
        subprocess.run(reset_dns_cmd, shell=True, check=True, text=True, capture_output=True)

        # Revert to using DNS from DHCP (if applicable)
        auto_dns_cmd = f"sudo nmcli connection modify '{connection_name}' ipv4.ignore-auto-dns no"
        subprocess.run(auto_dns_cmd, shell=True, check=True, text=True, capture_output=True)

        print(Fore.CYAN + f"Applying changes to connection '{connection_name}'..." + Style.RESET_ALL)
        apply_cmd = f"sudo nmcli connection up '{connection_name}'"
        result = subprocess.run(apply_cmd, shell=True, check=True, text=True, capture_output=True)
        if result.stdout and "successfully activated" in result.stdout:
            print(Fore.CYAN + result.stdout.strip() + Style.RESET_ALL)
        elif result.stderr:
             print(Fore.YELLOW_EX + result.stderr.strip() + Style.RESET_ALL)
        
        # The original script restarted NetworkManager.
        # 'nmcli con up' should be sufficient in most cases.
        # If /etc/resolv.conf doesn't update correctly, restarting NM might be a more forceful option.
        # For now, we rely on 'nmcli con up'.

        print(Fore.LIGHTGREEN_EX + "DNS servers reset successfully." + Style.RESET_ALL)
        print(Fore.YELLOW_EX + "You might need to restart your browser or application for changes to take full effect." + Style.RESET_ALL)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error executing command: {e.cmd}" + Style.RESET_ALL)
        error_output = ""
        if e.stdout:
            error_output += f"Stdout: {e.stdout.strip()}\\n"
        if e.stderr:
            error_output += f"Stderr: {e.stderr.strip()}"
        if error_output:
            print(Fore.RED + error_output + Style.RESET_ALL)
        print(Fore.RED + "Failed to reset DNS." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred while resetting DNS: {e}" + Style.RESET_ALL)

# Function to prompt user to select an option from the list
def prompt_user(options, question, show_exit=True):
    print(Fore.LIGHTYELLOW_EX + question + Style.RESET_ALL)
    # Calculate the maximum length of options
    max_length = max(len(option) for _, option in options) + 6
    # Draw a rectangle around the options
    print(Fore.LIGHTBLUE_EX + "+" + "-" * (max_length + 2) + "+" + Style.RESET_ALL)
    for i, option in options:
        # Adjust the length of the option title
        option_title = f"{i}. {option}".ljust(max_length)
        print(Fore.LIGHTBLUE_EX + f"| {option_title} |" + Style.RESET_ALL)
    # Draw the exit option
    if show_exit: # Conditional drawing of exit option
        exit_option = "0. Exit".ljust(max_length)
        print(Fore.LIGHTBLUE_EX + f"| {exit_option} |" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + "+" + "-" * (max_length + 2) + "+" + Style.RESET_ALL)
    while True:
        try:
            choice = input("Enter the number of your choice: ").strip()
            if choice.isdigit():
                choice_int = int(choice)
                if show_exit and choice_int == 0:
                    return "Exit"
                elif 1 <= choice_int <= len(options):
                    return options[choice_int - 1][1]
                else:
                    print(Fore.RED + "Invalid choice. Please enter a number within the range." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)

def main_cli():
    # Print ASCII art with colors
    ascii_art = """
             _                        __                      
     /\   /\(_) _ __    ___  _ __    / /   ___    ___   _ __  
     \ \ / /| || '_ \  / _ \| '__|  / /   / _ \  / _ \ | '_ \ 
      \ V / | || |_) ||  __/| |    / /___| (_) || (_) || |_) |
       \_/  |_|| .__/  \___||_|    \____/ \___/  \___/ | .__/ 
               |_|                                     |_|      """

    print(Fore.LIGHTBLUE_EX + ascii_art )
    print(Fore.LIGHTRED_EX + "                                                              Ver1.0" + Style.RESET_ALL)
    dns_action = prompt_user([(1, "Set DNS"), (2, "Reset DNS")], "Do you want to set or reset DNS?", show_exit=True)

    if dns_action == "Set DNS":
        # Find active network cards
        active_cards = find_active_network_cards()
        if not active_cards:
            print(Fore.RED + "No active network cards found." + Style.RESET_ALL)
            sys.exit(1)


        # Prompt user to select a network card
        selected_network_card = prompt_user([(i, option) for i, option in enumerate(active_cards, start=1)], "Select a network card:", show_exit=False) # show_exit is False as exiting here is not logical

        # Prompt user to select DNS servers
        dns_options = [
            "Electro",
            "403.Online",
            "Radargame",
            "Shatel",
            "Shecan",
            "Bogzar",
            "Google",
            "Open DNS",
            "Quad9",
            "Cloud Flare",
            "Comodo",
            "AdGuard",
            "Norton",
            "Clean",
            "Yandex",
            "Level 3",
            # Add more DNS options here
        ]
        selected_dns = prompt_user([(i, option) for i, option in enumerate(dns_options, start=1)], "Select DNS server:", show_exit=True)

        # Exit option
        if selected_dns == "Exit":
            sys.exit(0)

        # Extract DNS server IPs from selected option
        dns_servers = {
            "Electro": ("78.157.42.101", "78.157.42.100"),
            "403.Online": ("10.202.10.202", "10.202.10.102"),
            "Radargame": ("10.202.10.10", "10.202.10.11"),
            "Shatel": ("85.15.1.14", "85.15.1.15"),
            "Shecan": ("178.22.122.100", "185.51.200.2"),
            "Bogzar": ("185.55.226.26", "185.55.225.25"),
            "Google": ("8.8.8.8", "8.8.4.4"),
            "Open DNS": ("208.67.222.222", "208.67.220.220"),
            "Quad9": ("9.9.9.9", "149.112.112.112"),
            "Cloud Flare": ("1.1.1.1", "1.0.0.1"),
            "Comodo": ("8.26.56.26", "8.20.247.20"),
            "AdGuard": ("94.140.14.14", "94.140.15.15"),
            "Norton": ("199.85.126.10", "199.85.126.20"),
            "Clean": ("185.228.168.168", "185.228.169.168"),
            "Yandex": ("77.88.8.8", "77.88.8.1"),
            "Level 3": ("209.244.0.3", "209.244.0.4"),
            # Add more DNS servers here
        }
        dns_server1, dns_server2 = dns_servers.get(selected_dns, ("", ""))
        
        # Check if DNS IPs were actually found for the selection
        if not dns_server1 and not dns_server2 and selected_dns not in dns_servers: # Check if it's an actual missing key
            print(Fore.RED + f"DNS IP addresses for '{selected_dns}' are not defined in the script. Cannot set DNS." + Style.RESET_ALL)
            sys.exit(1)

        # Set DNS servers
        set_dns(selected_network_card, dns_server1, dns_server2)

    elif dns_action == "Reset DNS":
        # Find active network cards
        active_cards = find_active_network_cards()
        if not active_cards:
            print(Fore.RED + "No active network cards found." + Style.RESET_ALL)
            sys.exit(1)

        # Prompt user to select a network card
        selected_network_card = prompt_user([(i, option) for i, option in enumerate(active_cards, start=1)], "Select a network card:", show_exit=False) # show_exit is False as exiting here is not logical

        # Reset DNS
        reset_dns(selected_network_card)

    # Exiting the program
    elif dns_action == "Exit":
        sys.exit(0)

if __name__ == "__main__":
    main_cli()
