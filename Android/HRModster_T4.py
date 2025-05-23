import os
import re
import shutil
from tqdm import tqdm

# Define colors for terminal output
DARKGRAY = '\033[90m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
NOCOLOR = '\033[0m'
RED = '\033[1;31m'
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
# Banner
# Attribution and Redistribution Notice
print(f"{CYAN}Owner and Creator: @HRModster{NOCOLOR}")
print(f"{CYAN}Multi Search Tool{NOCOLOR}")
print(f"{RED}**The multi-search function filters for files containing all specified input strings, ignoring any files that do not meet this exact match criterion.**{NOCOLOR}")

# Directories
output_folder = "/data/data/com.termux/files/home/Tool/obb/unpacked_ASS_pak"
searched_dat = "/data/data/com.termux/files/home/Tool/obb/Searched_DAT"

def search_text():
    search_strings = []
    
    # Collect multiple search strings, skip empty entries
    while True:
        search_string = input("Enter a string to search for (or press enter to start search): ").strip()
        if not search_string:  # Prevent empty strings or Enter presses from being added
            if len(search_strings) == 0:
                print(f"{YELLOW}No search strings entered. Exiting...{NOCOLOR}")
                return
            else:
                break
        search_strings.append(search_string)
    
    # Collect all files in a list to show progress
    all_files = []
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            all_files.append(os.path.join(root, file))

    if not all_files:
        print(f"{YELLOW}No files found in {output_folder}.{NOCOLOR}")
        return

    search_results = []

    # Create a tqdm progress bar
    with tqdm(total=len(all_files), desc="Searching files") as pbar:
        for file_path in all_files:
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    file_content = f.read()
                    # Match all non-empty search strings in the file content (case-insensitive)
                    if all(re.search(re.escape(search_str), file_content, re.IGNORECASE) for search_str in search_strings):
                        search_results.append(file_path)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
            pbar.update(1)

    if not search_results:
        print(f"{YELLOW}No matching files found.{NOCOLOR}")
    else:
        # Sort search results by the file name (alphabetically)
        search_results = sorted(search_results, key=lambda x: os.path.basename(x))

        print(f"{CYAN}Matching files (sorted):{NOCOLOR}")
        for i, result in enumerate(search_results):
            print(f"{CYAN}{i+1}: {os.path.basename(result)}{NOCOLOR}")

        selected_files = []

        while True:
            choice = input("Enter file numbers to add to the selection (e.g., 2,5,6,4), 'a' to select all, or 'q' to quit: ")

            if choice == "q":
                print(f"{YELLOW}Operation canceled.{NOCOLOR}")
                break
            elif choice == "a":
                selected_files = search_results
                print(f"{CYAN}All files selected.{NOCOLOR}")
                break
            else:
                # Sort the file numbers entered by the user
                file_numbers = sorted(choice.split(','), key=lambda x: int(x) if x.isdigit() else float('inf'))
                for num in file_numbers:
                    if num.isdigit() and 1 <= int(num) <= len(search_results):
                        selected_files.append(search_results[int(num) - 1])
                        print(f"{CYAN}File '{os.path.basename(search_results[int(num) - 1])}' added to selection.{NOCOLOR}")
                    else:
                        print(f"{YELLOW}Invalid file number '{num}'. Try another one.{NOCOLOR}")

        if not selected_files:
            print(f"{YELLOW}No files selected for copying.{NOCOLOR}")
        else:
            print(f"{CYAN}Selected files (sorted):{NOCOLOR}")
            for file in selected_files:
                print(f"- {os.path.basename(file)}")

            if not os.path.exists(searched_dat):
                os.makedirs(searched_dat)
                print(f"{CYAN}Created directory '{searched_dat}'.{NOCOLOR}")

            copy_option = input("Enter 'c' to copy all files with the same base names as selected files or 'q' to quit: ")
            if copy_option == "c":
                # Get base names of selected files
                base_names = {os.path.splitext(os.path.basename(file))[0] for file in selected_files}

                # Copy files with the same base names
                for root, dirs, files in os.walk(output_folder):
                    for file in files:
                        base_name = os.path.splitext(file)[0]
                        if base_name in base_names:
                            src_path = os.path.join(root, file)
                            shutil.copy(src_path, searched_dat)
                            print(f"{CYAN}File '{file}' copied to the destination directory.{NOCOLOR}")
            else:
                print(f"{YELLOW}Operation canceled.{NOCOLOR}")

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
    search_text()
