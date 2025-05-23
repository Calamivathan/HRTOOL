import os
from tqdm import tqdm
import subprocess

class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'

def list_folders(base_directory):
    """List folders in the base directory."""
    folders = [folder for folder in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, folder))]
    if not folders:
        print("No folders found in the base directory.")
        return None
    print("Available folders:")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}: {folder}")
    return folders

def select_folder(base_directory):
    """Let the user select a folder."""
    folders = list_folders(base_directory)
    if not folders:
        return None
    try:
        folder_index = int(input("Enter the number of the folder to search in: ")) - 1
        if folder_index < 0 or folder_index >= len(folders):
            raise ValueError
        return os.path.join(base_directory, folders[folder_index])
    except ValueError:
        print("Invalid selection.")
        return None

def get_search_entries(search_type):
    """Get search entries from the user."""
    search_entries = input(f"Enter the {'strings' if search_type == 'string' else 'hex patterns'} to search (comma-separated): ").split(',')
    search_entries = [entry.strip() for entry in search_entries if entry.strip()]
    if not search_entries:
        print("No valid search entries provided.")
        return None

    if search_type == 'string':
        hex_entries = [entry.encode('utf-8').hex() for entry in search_entries]
        print("\nHex representations of the entered strings:")
        for i, hex_entry in enumerate(hex_entries, start=1):
            print(f"{i}: {hex_entry}")
        search_entries = [bytes.fromhex(hex_entry) for hex_entry in hex_entries]
    elif search_type == 'hex':
        try:
            search_entries = [bytes.fromhex(entry) for entry in search_entries]
        except ValueError:
            print("Invalid hex pattern provided.")
            return None

    return search_entries

def search_files_hex(selected_folder, search_entries):
    """Search for files containing all hex search entries."""
    print("Searching files...")
    file_paths = [os.path.join(root, file_name) for root, _, files in os.walk(selected_folder) for file_name in files]

    found_files = []
    for file_path in tqdm(file_paths, desc="Progress", unit="file"):
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                if all(entry in file_data for entry in search_entries):
                    found_files.append(file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return found_files

def search_files_string(selected_folder, search_strings):
    """Case-insensitive string search."""
    print("Searching files (case-insensitive string search)...")
    file_paths = [os.path.join(root, file_name) for root, _, files in os.walk(selected_folder) for file_name in files]

    search_strings = [s.lower() for s in search_strings if s.strip()]
    found_files = []

    for file_path in tqdm(file_paths, desc="Progress", unit="file"):
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                printable_data = ''.join([chr(byte) for byte in file_data if 32 <= byte <= 126]).lower()
                if all(s in printable_data for s in search_strings):
                    found_files.append(file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

    return found_files

def save_files(found_files):
    """Save found files based on user selection."""
    if not found_files:
        print("\nNo files found containing all search entries.")
        return

    print("\nFiles containing all search entries:")
    for i, file in enumerate(found_files, start=1):
        print(f"{i}: {file}")

    save_option = input("\nPress 'a' to save all files, or enter file numbers separated by commas (e.g., 1,3,5): ").strip()

    output_directory = '/data/data/com.termux/files/home/Tool/obb/searched_zsdic'
    os.makedirs(output_directory, exist_ok=True)

    if save_option.lower() == 'a':
        for file_path in found_files:
            file_name = os.path.basename(file_path)
            destination = os.path.join(output_directory, file_name)
            try:
                with open(file_path, 'rb') as src, open(destination, 'wb') as dst:
                    dst.write(src.read())
                print(f"Saved: {destination}")
            except Exception as e:
                print(f"Error saving {file_path}: {e}")
    else:
        try:
            selected_indices = [int(index.strip()) - 1 for index in save_option.split(',')]
            for i in selected_indices:
                if 0 <= i < len(found_files):
                    file_path = found_files[i]
                    file_name = os.path.basename(file_path)
                    destination = os.path.join(output_directory, file_name)
                    with open(file_path, 'rb') as src, open(destination, 'wb') as dst:
                        dst.write(src.read())
                    print(f"Saved: {destination}")
                else:
                    print(f"Invalid file number: {i + 1}")
        except ValueError:
            print("Invalid input.")
def execute_script(script_path):
    if os.path.isfile(script_path):
        os.chmod(script_path, 0o777)
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
    else:
        print(f"{Colors.RED}{script_path} does not exist.{Colors.NOCOLOR}")

def main():
    base_directory = '/data/data/com.termux/files/home/Tool/obb/'

    while True:
        print("\nMain Menu:")
        print("1: String search (case-sensitive)")
        print("2: Hex search")
        print("3: String search (case-insensitive)")
        print("4: Min Menu")
        print("5: Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice in [1, 2, 3]:
            selected_folder = select_folder(base_directory)
            if not selected_folder:
                continue

            if choice == 1:
                search_entries = get_search_entries('string')
                if not search_entries:
                    continue
                found_files = search_files_hex(selected_folder, search_entries)
            elif choice == 2:
                search_entries = get_search_entries('hex')
                if not search_entries:
                    continue
                found_files = search_files_hex(selected_folder, search_entries)
            elif choice == 3:
                search_strings = input("Enter strings to search (comma-separated): ").split(',')
                search_strings = [s.strip() for s in search_strings if s.strip()]
                if not search_strings:
                    print("No valid search strings provided.")
                    continue
                found_files = search_files_string(selected_folder, search_strings)

            save_files(found_files)

        elif choice == 4:
            sscript_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T1"
            execute_script(sscript_path)

        elif choice == 5:
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
