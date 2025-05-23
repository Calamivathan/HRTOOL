import os
import subprocess
import sys
import shutil
import time
from tqdm import tqdm
import threading
import csv

# Define colors for terminal output
NOCOLOR = '\033[0m'
DARKGRAY = '\033[1;30m'
YELLOW = '\033[1;33m'
CYAN = '\033[1;36m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
BLUE = '\033[1;34m'
LIGHTGREEN = '\033[1;92m'
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
# Directories
csv_filepath = "/data/data/com.termux/files/home/Tool/obb/unpacked_ASS_pak/names.csv"
original_pak = "/data/data/com.termux/files/home/Tool/obb/Original_pak"
unpacked_pak = "/data/data/com.termux/files/home/Tool/obb/unpacked_pak"
repacked_pak = "/data/data/com.termux/files/home/Tool/obb/repacked_pak"
searched_dat = "/data/data/com.termux/files/home/Tool/obb/Searched_DAT"
god_files = "/data/data/com.termux/files/home/Tool/obb/HRModster_God_Files"
quickbms = "/data/data/com.termux/files/home/Tool/HRModster_EXES"
edited_dat = "/data/data/com.termux/files/home/Tool/obb/Edited_Dat"
Edited_DEASS_DAT= "/data/data/com.termux/files/home/Tool/obb/Edited_DEASS_DAT"
bms_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/script.bms"
unpacked_ASS_pak = "/data/data/com.termux/files/home/Tool/obb/unpacked_ASS_pak"
start_pattern_uasset = bytes.fromhex("C1 83 2A 9E")
start_pattern_lua = bytes.fromhex("1B 4C 75 61")
end_pattern_to_match = bytes.fromhex("C1 83 2A 9E")

bms_content = """23205a535444207363616e6e65720a232068747470733a2f2f6769746875622e636f6d2f66616365626f6f6b2f7a7374642f626c6f622f6465762f646f632f7a7374645f636f6d7072657373696f6e5f666f726d61742e6d640a0a6765742046494c4553206173697a650a636f6d74797065207a7374640a6d6174682072756e74696d6564203d20300a6d6174682066696c65636f756e74203d20300a666f722049203d2030203c2046494c45530a2020202069662072756e74696d6564203d3d2066696c65636f756e740a20202020202020737472696e67206e616d657a203d2022220a202020202020206d6174682066696c65636f756e74202b20310a20202020656e6469660a200a20202020737472696e67206e616d65203d206e616d657a0a20202020737472696e67206e616d65737a20702022253038642220690a20202020737472696e67206e616d65202b206e616d65737a0a20202020737472696e67206e616d65202b20222e646174220a2020202066696e646c6f63204f46465345542062696e61727920225c7832385c7862355c7832665c786664220a20202020676f746f204f46465345540a0a202020206964737472696e6720225c7832385c7862355c7832665c786664220a2020202073617665706f732062310a0a20202020676574626974732044696374696f6e6172795f49445f666c616720320a2020202073617665706f732062310a0a202020206765746269747320436f6e74656e745f436865636b73756d5f666c616720310a2020202073617665706f732062310a0a20202020676574626974732052657365727665645f62697420310a2020202073617665706f732062310a202020200a202020206765746269747320556e757365645f62697420310a2020202073617665706f732062310a202020200a20202020676574626974732053696e676c655f5365676d656e745f666c616720310a2020202073617665706f732062310a202020200a2020202067657462697473204672616d655f436f6e74656e745f53697a655f666c616720320a2020202073617665706f732062310a0a2020202069662053696e676c655f5365676d656e745f666c6167203d3d20300a20202020202020206765742057696e646f775f44657363726970746f7220627974650a202020202020202073617665706f732062310a20202020656e6469660a0a202020206966204672616d655f436f6e74656e745f53697a655f666c6167203d3d20300a202020202020202069662053696e676c655f5365676d656e745f666c6167203d3d2030202020202023204643535f4669656c645f53697a6520300a2020202020202020202020206d617468204672616d655f436f6e74656e745f53697a65203d20300a2020202020202020656c73652020202020202020202020202020202020202020202020202020202023204643535f4669656c645f53697a6520310a202020202020202020202020676574204672616d655f436f6e74656e745f53697a6520627974650a2020202020202020656e6469660a20202020656c6966204672616d655f436f6e74656e745f53697a655f666c6167203d3d203120202023204643535f4669656c645f53697a6520320a2020202020202020676574204672616d655f436f6e74656e745f53697a652073686f72740a202020202020200a20202020202020206d617468204672616d655f436f6e74656e745f53697a65202b203235360a20202020202020200a20202020656c6966204672616d655f436f6e74656e745f53697a655f666c6167203d3d203220202023204643535f4669656c645f53697a6520340a2020202020202020676574204672616d655f436f6e74656e745f53697a65206c6f6e670a20202020202020200a20202020656c6966204672616d655f436f6e74656e745f53697a655f666c6167203d3d203320202023204643535f4669656c645f53697a6520380a2020202020202020676574204672616d655f436f6e74656e745f53697a65206c6f6e676c6f6e670a20202020202020200a20202020656e6469660a20202020646f0a202020202020202067657462697473204c6173745f426c6f636b20310a202020202020200a20202020202020206765746269747320426c6f636b5f5479706520320a20202020202020200a20202020202020206765746269747320426c6f636b5f53697a652032310a202020202020200a2020202020202020696620426c6f636b5f54797065203d3d203120202320524c455f426c6f636b0a202020202020202020202020676f746f20312020202020202020202030205345454b5f4355520a2020202020202020656c73650a202020202020202020202020676f746f20426c6f636b5f53697a652030205345454b5f4355520a2020202020202020656e6469660a2020202020202020696620436f6e74656e745f436865636b73756d5f666c616720213d20300a20202020202020202020202067657420436f6e74656e745f436865636b73756d206c6f6e670a2020202020202020656e6469660a202020207768696c65204c6173745f426c6f636b203d3d20300a2020202073617665706f732053495a450a202020206d6174682053495a45202d204f46465345540a0a20202020636c6f67206e616d65204f46465345542053495a45204672616d655f436f6e74656e745f53697a650a6e65787420490a
"""

def delete_zone_identifiers(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".Identifier"):
                os.remove(os.path.join(root, file))

def makee():
    # Directory path
    dir_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES"
    bms_content1 = bytes.fromhex(bms_content)
    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

    # File name and full path
    file_name = "script.bms"
    bms_path = os.path.join(dir_path, file_name)
    with open(bms_path, 'wb') as file:
        file.write(bms_content1)

def show_banner():
    os.system('clear')
    print(f"{DARKGRAY}    )   (        *         )    (       (                     (     ")
    print(f"{DARKGRAY} ( /(   )\ )   (  `     ( /(    )\ )    )\ )    *   )         )\ )  ")
    print(f"{YELLOW} )\()) (()/(   )\))(    )\())  (()/(   (()/(  ` )  /(   (    (()/(  ")
    print(f"{YELLOW}((_)\   /(_)) ((_)()\  ((_)\    /(_))   /(_))  ( )(_))  )\    /(_)) ")
    print(f"{DARKGRAY} _((_) (_))   (_()((_)   ((_)  (_))_   (_))   (_(_())  ((_)  (_))   ")
    print(f"{DARKGRAY}| || | | _ \  |  \/  |  / _ \   |   \  / __|  |_   _|  | __| | _ \  ")
    print(f"{DARKGRAY}| __ | |   /  | |\/| | | (_) |  | |) | \__ \    | |    | _|  |   /  ")
    print(f"{DARKGRAY}|_||_| |_|_\  |_|  |_|  \___/   |___/  |___/    |_|    |___| |_|_\  ")
    print(f"{YELLOW}                                                                    {NOCOLOR}")

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
                new_file_name = f"{new_file_number:08d}.dat"
                chunk_file_path = os.path.join(output_folder, new_file_name)

                with open(chunk_file_path, "wb") as chunk_file:
                    chunk_file.write(chunk_data)

                print(f"Created chunk: {new_file_name}")

def ensure_directory(path):
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)

def get_chunk_size(file_path):
    return os.path.getsize(file_path)

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



# Function to check headers and rename files accordingly
def rename_files_based_on_headers_and_last_bytes(folder):
    delete_zone_identifiers(folder)
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
    file_list = get_files_in_folder(unpacked_ASS_pak)
    write_files_to_csv(file_list,unpacked_ASS_pak)
    print(f"File names have been written to 'names.csv' with {len(file_list)} entries.")


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

def delete_bms_file_after_delay(file_path, delay=4):
    """Function to delete the specified file after a given delay."""
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
        #print(f"File '{file_path}' deleted after {delay} seconds.")


def unpak64(selected_file):
    makee()
    try:
        # Update the path to use the correct user path if necessary
        subprocess.run(['chmod', '777', f"{quickbms}/quickbms_4gb_files"], check=True)
        subprocess.run(['chmod', '777', bms_path], check=True)
        subprocess.run(['chmod', '777', selected_file], check=True)
        subprocess.run(['chmod', '777', unpacked_pak], check=True)
        # Start the deletion thread
        deletion_thread = threading.Thread(target=delete_bms_file_after_delay, args=(bms_path, 5))
        deletion_thread.start()
        subprocess.run([f"{quickbms}/quickbms_4gb_files", "-e", "-w", bms_path, f"{original_pak}/{os.path.basename(selected_file)}", unpacked_pak], check=True)
        deletion_thread.join()
        ensure_directory(unpacked_pak)
        ensure_directory(unpacked_ASS_pak)
        reassemble_chunks(unpacked_pak, unpacked_ASS_pak)
    except subprocess.CalledProcessError as e:
        pass  # Suppress the error
    # update_csv_with_new_names(unpacked_ASS_pak)
    time.sleep(3)
    modeoptions()

def unpacking(selected_file):
    print(f"{CYAN}Choose the system bit:{NOCOLOR}")
    print("1. 32/64-bit ")
    print("2. back to menu")
    bit_choice = input("Enter your choice (1 or 2): ")
    
    if bit_choice == '1':
        unpak64(selected_file)
        modeoptions()
    elif bit_choice == '2':
        modeoptions()
    else:
        print(f"{RED}Invalid option. Exiting.{NOCOLOR}")
        exit(1)

def unpack():
    print(f"{YELLOW}Starting Unpacking PAK files...{NOCOLOR}")
    delete_zone_identifiers(original_pak)
    try:
        os.chdir(original_pak)
    except FileNotFoundError:
        print(f"Directory not found: {original_pak}")
        exit(1)

    pak_files = [f for f in os.listdir(original_pak) if f.endswith('.pak')]
    if not pak_files:
        print(f"{RED}No PAK files found in {original_pak}.{NOCOLOR}")
        modeoptions()
        return

    print("Available PAK files:")
    for i, pak_file in enumerate(pak_files, 1):
        print(f"{i}. {pak_file}")

    try:
        choice = int(input("Select a PAK file to unpack: ")) - 1
        selected_file = pak_files[choice]
    except (ValueError, IndexError):
        print(f"{RED}Invalid selection. Please choose a valid file.{NOCOLOR}")
        unpack()
        return

    print(f"{GREEN}Selected file: {selected_file}{NOCOLOR}")
    os.makedirs(unpacked_pak, exist_ok=True)
    unpacking(selected_file)
    print(f"{LIGHTGREEN}Unpacking complete.{NOCOLOR}")
    print()
    modeoptions()

def repak64(selected_file):
    makee()
    subprocess.run(['chmod', '777', f"{quickbms}/quickbms_4gb_files"], check=True)

    try:
        ensure_directory(Edited_DEASS_DAT)
        delete_zone_identifiers(edited_dat)
        delete_zone_identifiers(Edited_DEASS_DAT)
        restore_original_names(csv_filepath, edited_dat)
        deassemble_files(edited_dat, Edited_DEASS_DAT)
        # Update the path to use the correct user path if necessary
        subprocess.run(['chmod', '777', bms_path], check=True)

        # Start the deletion thread
        deletion_thread = threading.Thread(target=delete_bms_file_after_delay, args=(bms_path, 5))
        deletion_thread.start()

        subprocess.run([f"{quickbms}/quickbms_4gb_files", "-w", "-r", bms_path, selected_file, Edited_DEASS_DAT], check=True)
        deletion_thread.join()
    except subprocess.CalledProcessError as e:
        pass  # Suppress the error

    time.sleep(5)
    modeoptions()

def repacking(selected_file):
    print("Please choose the PUBG mode bit:\n1. 32/64 bit both\n2. back to menu")
    bit = input("Choose (32bit or 64bit): ").strip()
    if bit == "1":
        repak64(selected_file)
        modeoptions()
    elif bit == "2":
        modeoptions()
    else:
        print(f"{RED}Invalid option. Exiting.{NOCOLOR}")
        modeoptions()

def repack():
    options = [os.path.join(original_pak, f) for f in os.listdir(original_pak) if f.endswith('.pak')]

    if not options:
        print(f"{RED}No PAK files found in {original_pak}.{NOCOLOR}")
        modeoptions()
        return

    print("Please select a file to repack:")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")

    try:
        choice = int(input("Choose an option: ")) - 1
        if 0 <= choice < len(options):
            selected_file = options[choice]
            print(f"You picked {selected_file} which is file {choice + 1}")

            os.makedirs(repacked_pak, exist_ok=True)
            repacked_file = os.path.join(repacked_pak, os.path.basename(selected_file))

            shutil.copy(selected_file, repacked_pak)
            print("copying...")
            selected_file = repacked_file

            repacking(selected_file)
        else:
            print(f"{RED}Invalid option. Try another one.{NOCOLOR}")
            repack()
    except ValueError:
        print(f"{RED}Invalid input. Please enter a number.{NOCOLOR}")
        repack()

def clear_old_pak():
    show_banner()
    print(f"{YELLOW}Clearing old PAK data...{NOCOLOR}")
    shutil.rmtree(unpacked_pak, ignore_errors=True)
    os.makedirs(unpacked_pak, exist_ok=True)
    shutil.rmtree(repacked_pak, ignore_errors=True)
    os.makedirs(repacked_pak, exist_ok=True)
    shutil.rmtree(unpacked_ASS_pak, ignore_errors=True)
    os.makedirs(unpacked_ASS_pak, exist_ok=True)
    print(f"{LIGHTGREEN}Old PAK data cleared.{NOCOLOR}")
    print()
    modeoptions()

def move_repacked_pak():
    show_banner()
    print(f"{YELLOW}Moving repacked PAK for processing...{NOCOLOR}")
    dest_pak_path = "/data/data/com.termux/files/home/Tool/obb/unpacked_obb/ShadowTrackerExtra/Content/Paks"
    if not os.path.exists(dest_pak_path):
        os.makedirs(dest_pak_path, exist_ok=True)
    if os.path.exists(repacked_pak):
        for item in os.listdir(repacked_pak):
            s = os.path.join(repacked_pak, item)
            d = os.path.join(dest_pak_path, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            elif os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
        print(f"{LIGHTGREEN}Repacked PAK has been moved for processing.{NOCOLOR}")
    else:
        print(f"{RED}Repacked PAK directory does not exist.{NOCOLOR}")
    print()
    modeoptions()

def Multi_Search():
    show_banner()
    print(f"{YELLOW}Searching in DAT files...{NOCOLOR}")
    subprocess.run(['chmod', '+x', '/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T4'])
    subprocess.run(['/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T4'])
    print(f"{LIGHTGREEN}Search complete.{NOCOLOR}")
    print()
    modeoptions()

def Compare_Files_in_Folder():
    show_banner()
    print(f"{YELLOW}Initiating God Search...{NOCOLOR}")
    subprocess.run(['chmod', '+x', '/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T5'])
    subprocess.run(['/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T5'])
    print(f"{LIGHTGREEN}God Search complete.{NOCOLOR}")
    print()
    modeoptions()

def delete_folder_data():
    # Dictionary of folder paths
    folders = {
        "1": "/data/data/com.termux/files/home/Tool/obb/Original_pak",
        "2": "/data/data/com.termux/files/home/Tool/obb/unpacked_pak",
        "3": "/data/data/com.termux/files/home/Tool/obb/repacked_pak",
        "4": "/data/data/com.termux/files/home/Tool/obb/Searched_DAT",
        "5": "/data/data/com.termux/files/home/Tool/obb/Edited_Dat",
        "6": "/data/data/com.termux/files/home/Tool/obb/Edited_DEASS_DAT",
        "7": "/data/data/com.termux/files/home/Tool/obb/unpacked_ASS_pak"
    }

    # Display options to the user
    print("Select the folder you want to delete:")
    for key, folder in folders.items():
        print(f"{key}: {folder}")

    # Get user's choice
    choice = input("Enter the number corresponding to the folder to delete: ")

    # Check if the input is valid
    if choice in folders:
        folder_path = folders[choice]
        
        if os.path.exists(folder_path):
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete all data inside {folder_path}? (y/n): ")
            if confirm.lower() == "y":
                # Delete all files and subdirectories inside the folder
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        if os.path.isdir(file_path):
                            shutil.rmtree(file_path)  # Remove directory and its contents
                        else:
                            os.remove(file_path)  # Remove file
                    except Exception as e:
                        print(f"Error while deleting {file_path}: {e}")
                print(f"All data in {folder_path} has been deleted.")
            else:
                print("Deletion canceled.")
        else:
            print(f"The folder {folder_path} does not exist.")
    else:
        print("Invalid choice. Please select a valid number.")
    modeoptions()

def modeoptions():
    show_banner()
    print(f"{YELLOW}Please choose an option:{NOCOLOR}")
    print("1. Unpack PAK")
    print("2. Repack PAK")
    print("3. Clear Old PAK Data")
    print("4. Move Repacked PAK For Processing")
    print("5. Multi Search")
    print("6. Compare Files in Folder")
    print("7. Delete Data")
    print("8. Back to main menu")
    print("9. Exit")

    try:
        mode_choice = int(input("Enter your choice: "))
    except ValueError:
        print(f"{RED}Invalid input. Please enter a number.{NOCOLOR}")
        modeoptions()
        return

    if mode_choice == 1:
        unpack()
    elif mode_choice == 2:
        repack()
    elif mode_choice == 3:
        clear_old_pak()
    elif mode_choice == 4:
        move_repacked_pak()
    elif mode_choice == 5:
        Multi_Search()
    elif mode_choice == 6:
        Compare_Files_in_Folder()
    elif mode_choice == 7:
        delete_folder_data()
    elif mode_choice == 8:
        print("Returning to Main Menu...")
        script_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T1"
        subprocess.run([script_path])
    elif mode_choice == 9:
        print(f"{GREEN}Exiting the program. Goodbye!{NOCOLOR}")
        exit(0)
    
    else:
        print(f"{RED}Invalid option. Please try again.{NOCOLOR}")
        modeoptions()



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
    modeoptions()
