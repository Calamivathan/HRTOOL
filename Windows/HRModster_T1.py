import os
import subprocess
import sys
import time
import requests

# Coloring
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'

def clear_screen():
    os.system('clear')

def show_banner():
    clear_screen()
    banner = f"""
{Colors.YELLOW}  _   _   ____    _____    ___     ___    _     
{Colors.YELLOW} | | | | |  _ \  |_   _|  / _ \   / _ \  | |    
{Colors.YELLOW} | |_| | | |_) |   | |   | | | | | | | | | |    
{Colors.YELLOW} |  _  | |  _ <    | |   | |_| | | |_| | | |___ 
{Colors.YELLOW} |_| |_| |_| \_\   |_|    \___/   \___/  |_____| 
{Colors.YELLOW}                                                 {Colors.NOCOLOR}
"""
    print(banner)
    print(msg_show)


def display_menu():
    show_banner()

    print("Thanks to all for your support")
    print()
    print(f"{Colors.BLUE}Tool Started{Colors.NOCOLOR}")
    print()
    print(f"{Colors.GREEN}1. OBB TOOL{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}2. OBB PAK TOOL{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}3. ZSDIC PAK TOOL{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}4. GAME PATCH TOOL{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}5. MAP PAK TOOL{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}6. AUTO SKIN TOOL{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}7. EXTRA FEATURES{Colors.NOCOLOR}")
    print(f"{Colors.RED}8. EXIT{Colors.NOCOLOR}")
    print()
    
    try:
        option = int(input("Choose an option [1-8]: "))
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number between 1 and 8.{Colors.NOCOLOR}")
        time.sleep(0.3)
        display_menu()
        return

    if option == 1:
        print("You selected OBB TOOL.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T2"
        execute_script(script_path)
    elif option == 2:
        print("You selected OBB PAK TOOL.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T3"
        execute_script(script_path)
    elif option == 3:
        print("You selected ZSDIC PAK TOOL.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T18"
        execute_script(script_path)
    elif option == 4:
        print("You selected GAME PATCH TOOL.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T8"
        execute_script(script_path)
    elif option == 5:
        print("You selected MAP PAK TOOL.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T13"
        execute_script(script_path)
    elif option == 6:
        print("You selected AUTO SKIN TOOL.")
        print("Auto Skin tool have been removed.")
        time.sleep(2)
        display_menu()
    elif option == 7:
        print("You selected EXTRA FEATURES.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T20"
        execute_script(script_path)
    elif option == 8:
        print("Exiting...")
        sys.exit(0)
    else:
        print(f"{Colors.RED}Invalid option. Please choose a number between 1 and 8.{Colors.NOCOLOR}")
        time.sleep(0.3)
        display_menu()

def execute_script(script_path):
    if os.path.isfile(script_path):
        os.chmod(script_path, 0o777)
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
    else:
        print(f"{Colors.RED}{script_path} does not exist.{Colors.NOCOLOR}")

def run_hasher_v2_and_verify():
    hrmodster_exes = "/data/data/com.termux/files/home/Tool/HRModster_EXES"
    hasher_v2_path = f"{hrmodster_exes}/hasher_v2"
    hasher_argument = "BJTYFukterc5648U5796V4679v6VB845c7iv578V675vOo89b6O8B7V5cv546ctvbjHVru3jNghwDKecCqWa6qRtz2Y3jYEEmwd93bMb6Tk="

    try:
        # Run the hasher_v2 program with the required argument
        result = subprocess.run([hasher_v2_path, hasher_argument], capture_output=True, text=True)
        
        # Get the output of the hasher_v2 execution
        hasher_output = result.stdout.strip()
        global msg_show
        msg_show = hasher_output
        hasher_output1 = hasher_output[-63:]
        print(f"{hasher_output}")
        if hasher_output1 == 'Verification Status From Server: Verified! Enjoy using the tool':
            return True  # Verification passed, continue the script
        else:
            print(f"{Colors.RED}Verification failed. Unexpected output{Colors.NOCOLOR}")
            return False  # Return False if verification fails

    except FileNotFoundError:
        print(f"{Colors.RED}Error: hasher_v2 executable not found at {hasher_v2_path}.{Colors.NOCOLOR}")
        return False  # Return False if the executable is not found
    except Exception as e:
        print(f"Error running hasher_v2: {e}")
        return False  # Return False on any other error


if __name__ == "__main__":
    if not run_hasher_v2_and_verify():
        sys.exit(1)  # Exit the program if verification failed

    display_menu()