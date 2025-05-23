import os
import shutil
import hashlib
from tqdm import tqdm
import subprocess
import sys
import time

# Constants and paths
GAMEPATCH_DIR = "/data/data/com.termux/files/home/Tool/obb"
OUTPUT_DIR = "/data/data/com.termux/files/home/Tool/obb/Compared_DAT"
EXES_DIR = "/data/data/com.termux/files/home/Tool/HRModster_EXES"
HASHER_V2_PATH = os.path.join(EXES_DIR, "hasher_v2")
HASHER_ARG = "21987654321098765432109876543210987654321098765432109876543210987654"
EXPECTED_HASH = "84321987654321098765432109876543210987654321098765432109876543210"

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

def list_and_select_folder(prompt):
    """List folders in GAMEPATCH_DIR and let the user select one."""
    folders = [f for f in os.listdir(GAMEPATCH_DIR) if os.path.isdir(os.path.join(GAMEPATCH_DIR, f))]
    
    if not folders:
        print(f"{Colors.RED}No folders found in {GAMEPATCH_DIR}.{Colors.NOCOLOR}")
        time.sleep(0.5)
        subprocess.run(['/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T3'], check=True)

    print(prompt)
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    try:
        choice = int(input("Select a folder: ")) - 1
        selected_folder = os.path.join(GAMEPATCH_DIR, folders[choice])
        print(f"{Colors.GREEN}Selected folder: {selected_folder}{Colors.NOCOLOR}")
        return selected_folder
    except (ValueError, IndexError):
        print(f"{Colors.RED}Invalid selection. Please choose a valid folder.{Colors.NOCOLOR}")
        return list_and_select_folder(prompt)

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_files(src, dst):
    ensure_directory(os.path.dirname(dst))
    shutil.copy2(src, dst)

def count_files(folder):
    """Count all files recursively in the folder."""
    total_files = 0
    for _, _, files in os.walk(folder):
        total_files += len(files)
    return total_files

def hash_file(filepath):
    """Generate a hash of the file to compare content."""
    hash_algo = hashlib.md5()  # You can use SHA256 if you prefer
    with open(filepath, 'rb') as file:
        while chunk := file.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def compare_folders(original_folder, changed_folder, output_folder, progress_bar, update_interval=500):
    original_output = os.path.join(output_folder, "original")
    changed_output = os.path.join(output_folder, "changed")

    ensure_directory(original_output)
    ensure_directory(changed_output)

    file_count = 0  # To track how many files have been processed

    for root, _, files in os.walk(original_folder):
        for file_name in files:
            original_file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(original_file_path, original_folder)
            changed_file_path = os.path.join(changed_folder, relative_path)

            # Check if file exists in both directories
            if os.path.exists(changed_file_path):
                # Compare file contents using hash
                if hash_file(original_file_path) != hash_file(changed_file_path):
                    # If different, copy both files to respective output folders
                    copy_files(original_file_path, os.path.join(original_output, relative_path))
                    copy_files(changed_file_path, os.path.join(changed_output, relative_path))
            else:
                # If file is missing in changed folder, consider it as changed
                copy_files(original_file_path, os.path.join(original_output, relative_path))

            file_count += 1
            if file_count % update_interval == 0:
                progress_bar.update(update_interval)

    remaining_files = file_count % update_interval
    if remaining_files > 0:
        progress_bar.update(remaining_files)

def main():
    # Select original and changed folders
    original_folder = list_and_select_folder("Select the original folder:")
    changed_folder = list_and_select_folder("Select the changed folder:")

    # Ensure permissions to access the folders
    subprocess.run(['chmod', '-R', '777', original_folder], check=True)
    subprocess.run(['chmod', '-R', '777', changed_folder], check=True)
    subprocess.run(['chmod', '-R', '777', OUTPUT_DIR], check=True)

    # Count total number of files in the original folder only
    total_files = count_files(original_folder)

    # Initialize tqdm progress bar
    with tqdm(total=total_files, desc="Comparing files", unit="file") as progress_bar:
        compare_folders(original_folder, changed_folder, OUTPUT_DIR, progress_bar)

    print(f"Differing files have been saved in {OUTPUT_DIR}")

if __name__ == "__main__":
    clear_screen()
    if run_hasher_v2_and_verify():  # Verify user before running the main program
        main()
    else:
        sys.exit(1)
