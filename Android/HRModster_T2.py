import os
import subprocess
import sys
import shutil
import time
import zipfile
from tqdm import tqdm

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

# Directories
ORIGINAL_OBB = "/data/data/com.termux/files/home/Tool/obb/Original_obb"
UNPACKED_OBB = "/data/data/com.termux/files/home/Tool/obb/unpacked_obb"
ORIGINAL_PAK = "/data/data/com.termux/files/home/Tool/obb/Original_pak"

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

def unpack_obb():
    show_banner()
    print(f"{Colors.YELLOW}Starting Unpacking OBB files...{Colors.NOCOLOR}")
    os.chdir(ORIGINAL_OBB)

    obb_files = [f for f in os.listdir() if f.endswith('.obb')]
    if not obb_files:
        print(f"{Colors.RED}No OBB files found in {ORIGINAL_OBB}.{Colors.NOCOLOR}")
        mode_options()
        return

    print("Available OBB files:")
    for i, obb_file in enumerate(obb_files, 1):
        print(f"{i}. {obb_file}")

    try:
        choice = int(input("Select an OBB file to unpack: ")) - 1
        obb_file = obb_files[choice]
    except (ValueError, IndexError):
        print(f"{Colors.RED}Invalid selection. Please choose a valid file.{Colors.NOCOLOR}")
        unpack_obb()
        return

    print(f"{Colors.GREEN}Selected file: {obb_file}{Colors.NOCOLOR}")
    obb_zip = f"{obb_file}.zip"
    print(f"{Colors.YELLOW}Renaming file to: {obb_zip}{Colors.NOCOLOR}")
    if os.path.exists(obb_zip):
        os.remove(obb_zip)  # Remove the existing file if it exists
    os.rename(obb_file, obb_zip)

    # Create a temporary zip file to measure progress
    with zipfile.ZipFile(obb_zip, 'r') as archive:
        total_files = len(archive.namelist())
        with tqdm(total=total_files, desc='Unpacking Archive') as pbar:
            for file_info in archive.infolist():
                archive.extract(file_info, path=UNPACKED_OBB)
                pbar.update(1)


    shutil.copy(obb_zip, UNPACKED_OBB)
    os.rename(obb_zip, obb_file)
    print(f"{Colors.LIGHTGREEN}DONE.{Colors.NOCOLOR}")
    print()
    mode_options()

def clear_old_obb():
    show_banner()
    print(f"{Colors.YELLOW}Clearing old OBB data...{Colors.NOCOLOR}")
    for filename in os.listdir(UNPACKED_OBB):
        file_path = os.path.join(UNPACKED_OBB, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"{Colors.RED}Failed to delete {file_path}. Reason: {e}{Colors.NOCOLOR}")
    print(f"{Colors.LIGHTGREEN}Old OBB data cleared.{Colors.NOCOLOR}")
    print()
    mode_options()

def copy_mini_obb_pak():
    show_banner()
    print("\033[93mCopying mini_obb.pak for processing...\033[0m")

    # Find the mini_obb.pak file in the unpacked_obb directory and its subdirectories
    mini_obb_pak_file = None
    for root, _, files in os.walk(UNPACKED_OBB):
        if 'mini_obb.pak' in files:
            mini_obb_pak_file = os.path.join(root, 'mini_obb.pak')
            break

    if mini_obb_pak_file:
        try:
            shutil.move(mini_obb_pak_file, ORIGINAL_PAK)
            print(f"\033[92mmini_obb.pak has been moved to {ORIGINAL_PAK}.\033[0m")
        except Exception as e:
            print(f"\033[91mError moving mini_obb.pak: {e}\033[0m")
    else:
        print(f"\033[91mmini_obb.pak not found in {UNPACKED_OBB}.\033[0m")

    print()
    mode_options()

def mode_options():
    show_banner()
    print(f"{Colors.BLUE}OBB TOOL Options{Colors.NOCOLOR}")
    print()
    print(f"{Colors.GREEN}1. Unpack OBB{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}2. Repack OBB{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}3. Clear Old OBB Data{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}4. Copy mini_obb.pak For Processing{Colors.NOCOLOR}")
    print(f"{Colors.GREEN}5. Back to Main Menu{Colors.NOCOLOR}")
    print(f"{Colors.RED}6. Exit{Colors.NOCOLOR}")
    print()

    try:
        option = int(input("Choose an option [1-6]: "))
    except ValueError:
        print(f"{Colors.RED}Invalid input. Please enter a number between 1 and 6.{Colors.NOCOLOR}")
        time.sleep(1)
        mode_options()
        return

    if option == 1:
        unpack_obb()
    elif option == 2:
        print("You selected Repack OBB.")
        os.system("chmod 777 /data/data/com.termux/files/home/Tool/obb/Original_obb")
        os.system("chmod 777 /data/data/com.termux/files/home/Tool/obb/Original_pak")
        os.system("chmod 777 /data/data/com.termux/files/home/Tool/obb/repacked_obb")
        os.system("chmod 777 /data/data/com.termux/files/home/Tool/obb/repacked_pak")
        subprocess.run(["chmod", "777", "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T7"])
        os.chdir("/data/data/com.termux/files/home/Tool/HRModster_EXES/")
        subprocess.run(['./HRModster_T7'], check=True)
    elif option == 3:
        clear_old_obb()
    elif option == 4:
        copy_mini_obb_pak()
    elif option == 5:
        print("Returning to Main Menu...")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T1"
        subprocess.run([script_path])
    elif option == 6:
        print("Exiting...")
        sys.exit(0)
    else:
        print(f"{Colors.RED}Invalid option. Please choose a number between 1 and 6.{Colors.NOCOLOR}")
        time.sleep(0.5)
        mode_options()


import subprocess
import sys

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
    # Run hasher_v2 and check verification
    if not run_hasher_v2_and_verify():
        sys.exit(1)  # Exit the program if verification failed

    # If verified, proceed with the mode options execution
    mode_options()
