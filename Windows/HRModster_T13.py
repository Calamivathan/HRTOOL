import os
import subprocess
import sys
import shutil
import time

# Coloring
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
    LIGHTGREEN = '\033[1;92m'

# Directories for map pak
MAPPATCH_DIR = "/data/data/com.termux/files/home/Tool/mappak"
UNPACKED_RAW_MAP = os.path.join(MAPPATCH_DIR, "unpacked_RAW_DAT")
UNPACKED_ASS_MAP = os.path.join(MAPPATCH_DIR, "unpacked_ASS_DAT")
EDITED_DEASS_MAP = os.path.join(MAPPATCH_DIR, "Edited_DEASS_DAT")
REPACKED_MAP = os.path.join(MAPPATCH_DIR, "repacked_pak")
SEARCHED_MAP = os.path.join(MAPPATCH_DIR, "Searched_DAT")
EDITED_MAP = os.path.join(MAPPATCH_DIR, "Edited_DAT")
COMPARED_MAP = os.path.join(MAPPATCH_DIR, "Compared_DAT")

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

def mode_options():
    show_banner()
    print(f"{Colors.BLUE}MAP PAK TOOL Options{Colors.NOCOLOR}")
    print()
    print(f"{Colors.GREEN}1. Unpack MAP PAK{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}2. Repack MAP PAK{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}3. Multi Search{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}4. Clear Old Data{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}5. Compare Files{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}6. Back to Main Menu{Colors.NOCOLOR}")
    print(f"{Colors.RED}7. Exit{Colors.NOCOLOR}")
    print()

    try:
        option = int(input("Choose an option [1-7]: "))
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number between 1 and 7.{Colors.NOCOLOR}")
        time.sleep(1)
        mode_options()
        return

    if option == 1:
        print("You selected Unpack MAP PAK.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T14"  # Script for unpacking map pak
        execute_script(script_path)
        mode_options()
    elif option == 2:
        print("You selected Repack MAP PAK.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T15"  # Script for repacking map pak
        execute_script(script_path)
        mode_options()
    elif option == 3:
        print("You selected Multi Search.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T16"  # Script for multi-search in map pak
        execute_script(script_path)
        mode_options()
    elif option == 4:
        print("Clearing old data...")
        clear_old_data()
        mode_options()
    elif option == 5:
        print("You selected Compare Files.")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T17"  # Script for comparing map pak files
        execute_script(script_path)
        mode_options()
    elif option == 6:
        print("Returning to Main Menu...")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T1"  # Main menu script
        subprocess.run([script_path])
    elif option == 7:
        print("Exiting...")
        sys.exit(0)
    else:
        print(f"{Colors.RED}Invalid option. Please choose a number between 1 and 7.{Colors.NOCOLOR}")
        time.sleep(0.5)
        mode_options()

def clear_old_data():
    files_to_remove = [
        UNPACKED_RAW_MAP,
        UNPACKED_ASS_MAP,
        EDITED_DEASS_MAP,
        REPACKED_MAP,
        SEARCHED_MAP,
        EDITED_MAP,
        COMPARED_MAP
    ]

    for file_path in files_to_remove:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                command = f"find {file_path} -type f | xargs rm -f"
                os.system(command)
                print(f"Removed all files from directory: {file_path}")
            else:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
        else:
            print(f"{Colors.YELLOW}{file_path} does not exist.{Colors.NOCOLOR}")

def execute_script(script_path):
    if os.path.isfile(script_path):
        os.chmod(script_path, 0o755)
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
        sys.exit(1)  # Exit if verification fails
    mode_options()
