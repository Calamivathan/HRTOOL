import os
import shutil
import subprocess
import sys
import csv
from tqdm import tqdm
import time
# Paths and constants
EDITED_DAT = "/data/data/com.termux/files/home/Tool/gamepatch/Edited_DAT"
EDITED_DEASS_DAT = "/data/data/com.termux/files/home/Tool/gamepatch/Edited_DEASS_DAT"
REPACKED_PAK = "/data/data/com.termux/files/home/Tool/gamepatch/repacked_pak"
ORIGINAL_PAK = "/data/data/com.termux/files/home/Tool/gamepatch/Original_pak"
EXES_DIR = "/data/data/com.termux/files/home/Tool/HRModster_EXES"
HRTool_PATH = os.path.join(EXES_DIR, "HRTool")
HASHER_V2_PATH = os.path.join(EXES_DIR, "hasher_v2")
HASHER_ARG = "21987654321098765432109876543210987654321098765432109876543210987654"
EXPECTED_HASH = "84321987654321098765432109876543210987654321098765432109876543210"
csv_filepath = "/data/data/com.termux/files/home/Tool/gamepatch/unpacked_ASS_DAT/names.csv"


def delete_zone_identifiers(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".Identifier"):
                os.remove(os.path.join(root, file))
# Colors for output messages 
class Colors:
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    NOCOLOR = '\033[0m'

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

def ensure_directory(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)

def list_and_select_file(folder_path):
    """List files in `folder_path` and prompt the user to select one."""
    delete_zone_identifiers(folder_path)
    files = [f for f in os.listdir(folder_path)]
    if not files:
        print(f"{Colors.RED}No files found in {folder_path}.{Colors.NOCOLOR}")
        time.sleep(0.5)
        subprocess.run(['/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T8'], check=True)

    print("Available files:")
    for idx, file_name in enumerate(files, 1):
        print(f"{idx}. {file_name}")
    
    try:
        choice = int(input("Select a file to repack by number: ")) - 1
        selected_file = files[choice]
        print(f"{Colors.GREEN}Selected file: {selected_file}{Colors.NOCOLOR}")
        return os.path.join(folder_path, selected_file)
    except (ValueError, IndexError):
        print(f"{Colors.RED}Invalid selection. Exiting.{Colors.NOCOLOR}")
        time.sleep(0.5)
        subprocess.run(['/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T8'], check=True)

def copy_file_to_repack(input_file, output_dir):
    """Copy selected file from `Original_pak` to `repacked_pak`."""
    ensure_directory(output_dir)
    destination_path = os.path.join(output_dir, os.path.basename(input_file))
    shutil.copy2(input_file, destination_path)
    print(f"Copied {os.path.basename(input_file)} to {output_dir}")
    return destination_path

def deassemble_files(input_folder, output_folder):
    """Deassemble files in `input_folder` into 64 KB chunks in `output_folder`."""
    ensure_directory(output_folder)

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)

        with open(file_path, "rb") as input_file:
            file_data = input_file.read()
            size = len(file_data)

            # Number of chunks (64 KB each)
            num_chunks = size // 65536 + (1 if size % 65536 != 0 else 0)
            original_number = int(file_name.split('.')[0])  # Assuming file names are like '000000074.uasset'

            # Create chunks
            for chunk_index in range(num_chunks):
                chunk_data = file_data[chunk_index * 65536:(chunk_index + 1) * 65536]
                new_file_number = original_number + chunk_index
                new_file_name = f"{new_file_number:09d}.dat"
                chunk_file_path = os.path.join(output_folder, new_file_name)

                with open(chunk_file_path, "wb") as chunk_file:
                    chunk_file.write(chunk_data)

                print(f"Created chunk: {new_file_name}")

def restore_original_names(csv_filepath, folder_path):
    """
    Restores modified file names in the specified folder to their original names
    based on the mapping in the `names.csv` file.

    Args:
        csv_filepath (str): Path to the `names.csv` file.
        folder_path (str): Path to the folder containing the files to rename.

    Raises:
        FileNotFoundError: If `names.csv` or the folder doesn't exist.
    """
    # Ensure both the CSV file and the folder exist
    if not os.path.exists(csv_filepath):
        raise FileNotFoundError(f"CSV file '{csv_filepath}' not found.")
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' not found.")

    # Read the CSV and create a mapping of new to old names
    new_to_old_map = {}
    with open(csv_filepath, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_name = row["new"]
            old_name = row["old"]
            if new_name:  # Only consider rows with a `new` value
                new_to_old_map[new_name] = old_name

    # Iterate through files in the folder and rename if needed
    for file_name in os.listdir(folder_path):
        if file_name in new_to_old_map:
            old_name = new_to_old_map[file_name]
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, old_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {file_name} -> {old_name}")

    print("File restoration complete.")



def repack_files(input_file_path, output_dir):
    """Repack files from `input_file_path` into `output_dir` using HRTool."""
    # ensure_directory(output_dir)
    print(input_file_path,"\n",output_dir)
    try:
        subprocess.run([HRTool_PATH, '-a', '-r', input_file_path, output_dir], check=True)
        print(f"{Colors.GREEN}Repacking completed successfully!{Colors.NOCOLOR}")
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}Repacking failed.{Colors.NOCOLOR}")

def main():
    # Select file from Original_pak
    print("Selecting file to repack from Original_pak...")
    selected_file_path = list_and_select_file(ORIGINAL_PAK)
    
    # Copy selected file to repacked_pak
    copied_file_path = copy_file_to_repack(selected_file_path, REPACKED_PAK)
    
    # Deassemble files
    print("Deassembling files...")
    delete_zone_identifiers(EDITED_DAT)
    delete_zone_identifiers(EDITED_DEASS_DAT)
    restore_original_names(csv_filepath, EDITED_DAT)
    deassemble_files(EDITED_DAT, EDITED_DEASS_DAT)
    
    # Repack files
    print("Repacking files...")
    repack_files(copied_file_path, EDITED_DEASS_DAT)

if __name__ == "__main__":
    clear_screen()
    if run_hasher_v2_and_verify():  # Verify user before running the main program
        main()
    else:
        sys.exit(1)
