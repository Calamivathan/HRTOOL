import os
import subprocess
import sys
import time
import csv
from tqdm import tqdm

# Colors for output messages
class Colors:
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    NOCOLOR = '\033[0m'

# Directories and paths
EXES_DIR = "/data/data/com.termux/files/home/Tool/HRModster_EXES"
ORIGINAL_PAK_DIR = "/data/data/com.termux/files/home/Tool/mappak/Original_pak"
UNPACKED_RAW_DAT_DIR = "/data/data/com.termux/files/home/Tool/mappak/unpacked_RAW_DAT"
HASHER_V2_PATH = os.path.join(EXES_DIR, "hasher_v2")
HASHER_ARG = "21987654321098765432109876543210987654321098765432109876543210987654"
EXPECTED_HASH = "84321987654321098765432109876543210987654321098765432109876543210"
# Folder where the chunks are extracted
input_folder = "/data/data/com.termux/files/home/Tool/mappak/unpacked_RAW_DAT"
# Folder to save the reassembled files
output_folder = "/data/data/com.termux/files/home/Tool/mappak/unpacked_ASS_DAT"
os.makedirs(output_folder, exist_ok=True)

# Hex patterns to match at the start and end of files
start_pattern_uasset = bytes.fromhex("C1 83 2A 9E")
start_pattern_lua = bytes.fromhex("1B 4C 75 61")
end_pattern_to_match = bytes.fromhex("C1 83 2A 9E")


# ------------------------------------------------------------------------------
def get_files_in_folder(folder_path):
    """
    Retrieve and sort all files in the specified folder.
    """
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return sorted(files)

def write_files_to_csv(file_list, folder_path, csv_filename="names.csv"):
    """
    Write the sorted file names to a CSV file in the `old` column.
    If the file does not exist, it creates it in the specified folder.
    """
    # Ensure the folder exists
    csv_filepath = os.path.join(folder_path, csv_filename)

    # Create and write the CSV
    with open(csv_filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["old", "new"])  # Write the header
        for file_name in file_list:
            writer.writerow([file_name, ""])  # Populate `old` column with file names, leave `new` empty

    print(f"CSV file created or updated at: {csv_filepath}") # Add file names with an empty `new` column

def change_names(folder_path):
    """
    Rename files based on the logic described, and return a mapping of old to new names.
    """
    delete_zone_identifiers(folder_path)  # Remove unwanted files
    files = sorted(os.listdir(folder_path))  # Sort files alphabetically
    last_uasset = None
    old_to_new = {}

    # Rename files
    with tqdm(total=len(files), desc="Renaming files", unit="file") as pbar:
        for file in files:
            file_path = os.path.join(folder_path, file)
            if file.endswith('.uasset'):
                last_uasset = file  # Keep track of the last seen uasset file
            elif file.endswith('.uexp') and last_uasset:
                new_name = last_uasset.replace('.uasset', '.uexp')
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
                old_to_new[file] = new_name
            pbar.update(1)
    return old_to_new


def update_csv_with_new_names(folder_path, csv_filename="names.csv"):
    """
    Update the `new` column in the CSV file with new file names after renaming.
    Assumes the CSV already exists with entries in the `old` column.
    """
    # Ensure the full path to the CSV file
    csv_filepath = os.path.join(folder_path, csv_filename)

    # Ensure the CSV exists, raise error if it doesn't
    # Ensure the CSV exists, create it if it doesn't
    if not os.path.exists(csv_filepath):
        with open(csv_filepath, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["old", "new"])
            writer.writeheader()
        print(f"CSV file created at: {csv_filepath}")


    # Run the renaming function and get old-to-new mapping
    old_to_new_map = change_names(folder_path)

    # Read the existing CSV
    rows = []
    with open(csv_filepath, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            old_name = row["old"]
            # Update the `new` column based on the mapping
            new_name = old_to_new_map.get(old_name, row["new"])  # Use the map if available
            rows.append({"old": old_name, "new": new_name})
    
    # Write back the updated CSV
    with open(csv_filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["old", "new"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file updated successfully at: {csv_filepath}")



def delete_zone_identifiers(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".Identifier"):
                os.remove(os.path.join(root, file))

# Function to get chunk size
def get_chunk_size(file_path):
    return os.path.getsize(file_path)

# Function to reassemble files based on the specified rules
def reassemble_chunks(input_folder, output_folder):
    # List to hold sorted chunks by offset
    chunks = []
    
    # Collect and sort chunk files by their offset
    for file_name in os.listdir(input_folder):
        # Parse the offset from the filename (e.g., "0x001f07d0.dat" to 0x001f07d0)
        try:
            offset = int(file_name.split('.')[0], 16)
        except ValueError:
            continue  # Skip files that don't have a hex offset in their name
        
        file_path = os.path.join(input_folder, file_name)
        size = get_chunk_size(file_path)
        chunks.append((offset, file_path, size))
    
    # Sort chunks by their offset
    chunks.sort()

    # List to keep track of chunks to combine
    current_group = []
    
    # Iterate through the sorted chunks
    for i, (offset, file_path, size) in enumerate(chunks):
        # If the size is 64 KB, add to current group
        if size == 65536:
            current_group.append(file_path)
        else:
            # For smaller size, add it to the current group and write out as one file
            if current_group:
                current_group.append(file_path)
                
                # Use the name of the first chunk as the output file name
                first_chunk_name = os.path.basename(current_group[0])
                output_file_path = os.path.join(output_folder, first_chunk_name)
                
                # Combine current group into a single file
                with open(output_file_path, "wb") as output_file:
                    for chunk in current_group:
                        with open(chunk, "rb") as chunk_file:
                            output_file.write(chunk_file.read())
                print(f"file: {output_file_path}")
                current_group = []
            else:
                # If there's no group, write the chunk as a standalone file
                standalone_file_path = os.path.join(output_folder, os.path.basename(file_path))
                with open(standalone_file_path, "wb") as output_file:
                    with open(file_path, "rb") as chunk_file:
                        output_file.write(chunk_file.read())
                print(f"created: {standalone_file_path}")

    # Handle remaining chunks in the last group
    if current_group:
        first_chunk_name = os.path.basename(current_group[0])
        output_file_path = os.path.join(output_folder, first_chunk_name)
        with open(output_file_path, "wb") as output_file:
            for chunk in current_group:
                with open(chunk, "rb") as chunk_file:
                    output_file.write(chunk_file.read())
        print(f"created: {output_file_path}")

    # Rename files based on their headers and last bytes
    rename_files_based_on_headers_and_last_bytes(output_folder)
    file_list = get_files_in_folder(output_folder)
    write_files_to_csv(file_list,output_folder)
    print(f"File names have been written to 'names.csv' with {len(file_list)} entries.")

# Function to check headers and rename files accordingly
def rename_files_based_on_headers_and_last_bytes(folder):
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        
        # Read the first 4 bytes of the file
        with open(file_path, "rb") as f:
            start_bytes = f.read(4)
            f.seek(-4, os.SEEK_END)
            last_bytes = f.read(4)
        
        # Check for specific starting patterns
        if start_bytes == start_pattern_uasset:
            new_file_path = os.path.splitext(file_path)[0] + ".uasset"
            os.rename(file_path, new_file_path)
            print(f"{os.path.basename(new_file_path)}")
        elif start_bytes == start_pattern_lua:
            new_file_path = os.path.splitext(file_path)[0] + ".lua"
            os.rename(file_path, new_file_path)
            print(f"{os.path.basename(new_file_path)}")
        elif last_bytes == end_pattern_to_match:
            # Rename file to have a .uexp extension if last bytes match the pattern
            new_file_path = os.path.splitext(file_path)[0] + ".uexp"
            os.rename(file_path, new_file_path)
            print(f"{os.path.basename(new_file_path)}")

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


def xor_decrypt_file(file_path, xor_key=0x79):
    # Read the entire file into memory
    with open(file_path, 'rb') as file:
        file_data = bytearray(file.read())

    # Perform XOR on each byte
    for i in range(len(file_data)):
        file_data[i] ^= xor_key

    # Save the modified data back to the file
    with open(file_path, 'wb') as file:
        file.write(file_data)

    print(f"File '{file_path}' has been decrypted and saved.")

def unpack():
    delete_zone_identifiers(ORIGINAL_PAK_DIR)
    # List all files in Original_pak directory
    pak_files = [f for f in os.listdir(ORIGINAL_PAK_DIR)]
    
    # Check if there are any files to unpack
    if not pak_files:
        print(f"{Colors.RED}No files found in {ORIGINAL_PAK_DIR}.{Colors.NOCOLOR}")
        return

    # Display available files
    print("Available files:")
    for i, pak_file in enumerate(pak_files, 1):
        print(f"{i}. {pak_file}")

    # Get user choice
    try:
        choice = int(input("Select a file to unpack: ")) - 1
        selected_file = pak_files[choice]
    except (ValueError, IndexError):
        print(f"{Colors.RED}Invalid selection. Please choose a valid file.{Colors.NOCOLOR}")
        unpack()  # Restart the selection process if the input is invalid
        return

    # Confirm selection
    print(f"{Colors.GREEN}Selected file: {selected_file}{Colors.NOCOLOR}")

    # Ensure unpacked_RAW_DAT directory exists
    if not os.path.exists(UNPACKED_RAW_DAT_DIR):
        os.makedirs(UNPACKED_RAW_DAT_DIR)
        print(f"Created directory: {UNPACKED_RAW_DAT_DIR}")

    # Construct paths
    
    input_file_path = os.path.join(ORIGINAL_PAK_DIR, selected_file)
    xor_decrypt_file(input_file_path)
    output_dir = UNPACKED_RAW_DAT_DIR

    # Run the HRTool command
    HRTool_path = os.path.join(EXES_DIR, "HRTool")
    try:
        print("Unpacking with HRTool...")
        subprocess.run([HRTool_path, '-a', input_file_path, output_dir], check=True)
        print(f"{Colors.GREEN}Unpacking completed successfully!{Colors.NOCOLOR}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error during unpacking: {e}{Colors.NOCOLOR}")
    xor_decrypt_file(input_file_path)

if __name__ == "__main__":
    clear_screen()
    if run_hasher_v2_and_verify():  # Verify user before unpacking
        unpack()
        reassemble_chunks(input_folder, output_folder)
        update_csv_with_new_names(output_folder)

    else:
        sys.exit(1)
