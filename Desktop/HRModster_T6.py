import os
from tqdm import tqdm
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
# Directory path
folder_path = '/data/data/com.termux/files/home/Tool/obb/unpacked_ASS_pak'
folder_path2 = '/data/data/com.termux/files/home/Tool/obb/Edited_Dat'

def delete_zone_identifiers(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".Identifier"):
                os.remove(os.path.join(root, file))

# Function to rename uexp files based on the corresponding uasset files
def change_names():
    # Get list of all files and sort them numerically
    delete_zone_identifiers(folder_path)
    files = sorted(os.listdir(folder_path))
    last_uasset = None

    # Initialize progress bar
    with tqdm(total=len(files), desc="Renaming files", unit="file") as pbar:
        for file in files:
            file_path = os.path.join(folder_path, file)
            if file.endswith('.uasset'):
                last_uasset = file  # Keep track of last seen uasset file
            elif file.endswith('.uexp') and last_uasset:
                new_name = last_uasset.replace('.uasset', '.uexp')
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
            pbar.update(1)

# Function to revert changes by moving the .uexp to +1 from .uasset
def revert_changes():
    # Get list of all files and sort them numerically
    files = sorted(os.listdir(folder_path2))
    delete_zone_identifiers(folder_path2)
    # Check if all files are only .uexp, and increment their names if true
    if all(file.endswith('.uexp') for file in files):
        with tqdm(total=len(files), desc="Renaming .uexp files", unit="file") as pbar:
            for file in files:
                # Extract the number part and increment it
                base_number = file.replace('.uexp', '')
                new_number = str(int(base_number) + 1).zfill(len(base_number))
                
                # Create the new file name and rename the file
                current_path = os.path.join(folder_path2, file)
                new_path = os.path.join(folder_path2, new_number + '.uexp')
                
                os.rename(current_path, new_path)
                pbar.update(1)
        return  # Exit after renaming .uexp files

    # Initialize progress bar for mixed files
    with tqdm(total=len(files), desc="Reverting files", unit="file") as pbar:
        for i in range(len(files) - 1):
            uasset_file = files[i]
            next_file = files[i + 1]

            if uasset_file.endswith('.uasset') and next_file.endswith('.uexp'):
                # Extract the number part from the uasset file and increment it for the uexp file
                uasset_number = uasset_file.replace('.uasset', '')
                new_uexp_number = str(int(uasset_number) + 1).zfill(len(uasset_number))

                # Create new uexp file name with incremented number
                new_name = new_uexp_number + '.uexp'
                current_uexp_path = os.path.join(folder_path2, next_file)
                new_uexp_path = os.path.join(folder_path2, new_name)

                os.rename(current_uexp_path, new_uexp_path)
            pbar.update(1)


# Menu for user selection
def menu():
    print("Select an option:")
    print("1. Change file names")
    print("2. Revert file names")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        change_names()
    elif choice == '2':
        revert_changes()
    else:
        print("Invalid choice. Please select 1 or 2.")


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
    menu()
