import os
import sys
import subprocess
import time
import sys

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

def display_banner():
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

def display_attribution():
    print()

def create_directories_and_set_permissions(directories):
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
        else:
            print(f"Directory already exists: {directory}")
        print(f"Setting permissions for {directory}")
        subprocess.run(['chmod', '777', directory])

def set_executable_permissions(directory):
    print(f"{Colors.GREEN}Setting executable permissions for all files in {directory}{Colors.NOCOLOR}")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                subprocess.run(['chmod', '777', file_path])
                print(f"{Colors.GREEN}Set executable permissions for {file_path}{Colors.NOCOLOR}")
            else:
                print(f"{Colors.RED}{file_path} is not a regular file.{Colors.NOCOLOR}")

def run_main_script():
    print(f"{Colors.GREEN}Running main script...{Colors.NOCOLOR}")
    time.sleep(0.3)
    main_script = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T1"
    subprocess.run(['chmod', '777', main_script])
    os.chdir("/data/data/com.termux/files/home/Tool/HRModster_EXES/")
    subprocess.run(['./HRModster_T1'], check=True)


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
        print("Verification failed or error occurred, exiting.")
        sys.exit(1)  # Exit the program if verification failed
    # Run hasher_v2 and check verification
    if not run_hasher_v2_and_verify():
        print("Verification failed or error occurred, exiting.")
        sys.exit(1)  # Exit the program if verification failed
    
    # If verified, proceed with the main execution
    clear_screen()
    display_banner()
    display_attribution()

    base_path = "/data/data/com.termux/files/home/Tool"
    
    # Directory structure inside obb
    obb_directories = [
        "Original_obb",
        "unpacked_obb",
        "repacked_obb",
        "Original_pak",
        "unpacked_pak",
        "repacked_pak",
        "Searched_DAT",
        "Edited_Dat",
        "Compared_DAT",
        "unpack_zsdic_pak",
        "repacked_zsdic",
        "original_zsdic_pak"
    ]

    # Directory structure inside gamepatch and mappak
    common_patch_directories = [
        "Original_pak",
        "unpacked_RAW_DAT",
        "unpacked_ASS_DAT",
        "Edited_DEASS_DAT",
        "repacked_pak",
        "Searched_DAT",
        "Edited_DAT",
        "Compared_DAT"
    ]

    # Create directories under obb
    create_directories_and_set_permissions([os.path.join(base_path, "obb", d) for d in obb_directories])

    # Create directories under gamepatch and mappak
    for folder in ["gamepatch", "mappak"]:
        create_directories_and_set_permissions([os.path.join(base_path, folder, d) for d in common_patch_directories])

    # Set executable permissions in HRModster_EXES
    hrmodster_exes = os.path.join(base_path, "HRModster_EXES")
    set_executable_permissions(hrmodster_exes)

    # Run the main script after verification
    run_main_script()
