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
        subprocess.call(f'sudo nmcli dev set {network_card} ipv4.dns "{dns_server1} {dns_server2}"', shell=True)
        print(Fore.LIGHTGREEN_EX + "DNS servers set successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error setting DNS: {e}" + Style.RESET_ALL)

# Function to reset DNS
def reset_dns(network_card):
    try:
        subprocess.call(f'sudo nmcli dev set {network_card} ipv4.dns ""', shell=True)
        subprocess.call('sudo systemctl restart NetworkManager', shell=True)
        print(Fore.LIGHTGREEN_EX + "DNS servers reset successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error resetting DNS: {e}" + Style.RESET_ALL)

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
