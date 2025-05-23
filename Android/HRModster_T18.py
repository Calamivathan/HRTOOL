import os
import zstandard as zstd
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys
import time
import shutil
# Configuration
MAGIC_NUMBER = b'\x28\xB5\x2F\xFD'
DICT_START_HEX = bytes.fromhex("37 A4 30 EC")
MAX_COMPRESSION_LEVEL = 22
MAX_WORKERS = 4  # Parallel threads for decompression
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'

# Paths
ORIGINAL_ZSDIC_PAK = "/data/data/com.termux/files/home/Tool/obb/original_zsdic_pak/mini_obbzsdic_obb.pak"
UNPACK_DIR = "/data/data/com.termux/files/home/Tool/obb/unpack_zsdic_pak"
EDITED_DAT_DIR = "/data/data/com.termux/files/home/Tool/obb/edited_dat_zsdic"
REPACKED_DIR = "/data/data/com.termux/files/home/Tool/obb/repacked_zsdic"
REPACKED_PAK = os.path.join(REPACKED_DIR, "mini_obbzsdic_obb.pak")


def Load_pak():
    destination_file = "/data/data/com.termux/files/home/Tool/obb/original_zsdic_pak/"
    source_file = "/data/data/com.termux/files/home/Tool/obb/unpacked_obb/ShadowTrackerExtra/Content/Paks/mini_obbzsdic_obb.pak"
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print("Error: Unpack the OBB first!")
        return

    # Ensure the destination directory exists
    destination_dir = os.path.dirname(destination_file)
    os.makedirs(destination_dir, exist_ok=True)

    # Copy the file
    try:
        shutil.copy(source_file, destination_file)
        print(f"Copied {source_file} to {destination_file}")
    except Exception as e:
        print(f"Error during file copy: {e}")
        return

    # Set permissions
    try:
        os.chmod(destination_file, 0o777)
        print(f"Set permissions to 777 for {destination_file}")
    except Exception as e:
        print(f"Error setting permissions: {e}")

def Move_pak():
    source_file = "/data/data/com.termux/files/home/Tool/obb/unpacked_obb/repacked_zsdic/mini_obbzsdic_obb.pak"
    destination_dir = "/data/data/com.termux/files/home/Tool/obb/unpacked_obb/ShadowTrackerExtra/Content/Paks/"
    destination_file = os.path.join(destination_dir, "mini_obbzsdic_obb.pak")

    # Check if source file exists
    if not os.path.exists(source_file):
        print("Error: Source file does not exist!")
        return

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Set permissions for source and destination directory
    try:
        os.chmod(source_file, 0o777)
        os.chmod(destination_dir, 0o777)
        print(f"Set permissions to 777 for source and destination directory.")
    except Exception as e:
        print(f"Error setting permissions: {e}")
        return

    # Remove the existing file at the destination if it exists
    if os.path.exists(destination_file):
        try:
            os.remove(destination_file)
            print(f"Removed existing file: {destination_file}")
        except Exception as e:
            print(f"Error removing existing file: {e}")
            return

    # Move the file from source to destination
    try:
        shutil.move(source_file, destination_file)
        print(f"Moved {source_file} to {destination_file}")
    except Exception as e:
        print(f"Error during file move: {e}")
        return

    # Set permissions for the moved file
    try:
        os.chmod(destination_file, 0o777)
        print(f"Set permissions to 777 for {destination_file}")
    except Exception as e:
        print(f"Error setting permissions: {e}")


# Function to extract the dictionary from the `.pak` file
def extract_dictionary(pak_file, start_hex):
    with open(pak_file, 'rb') as f:
        data = f.read()

    dict_start = data.find(start_hex)
    if dict_start == -1:
        raise ValueError("Unable to parse mini_obbzsdic_obb.pak file.")

    return data[dict_start:]

# Function to split and buffer segments
def split_segments(data, magic_number):
    split_indices = []
    start = 0
    while (start := data.find(magic_number, start)) != -1:
        split_indices.append(start)
        start += len(magic_number)
    split_indices.append(len(data))  # Add EOF

    segments = []
    for i in range(len(split_indices) - 1):
        segment_start = split_indices[i]
        segment_end = split_indices[i + 1]
        segments.append((i + 1, data[segment_start:segment_end]))
    return segments

# Function to decompress a single segment
def decompress_segment(segment, dictionary, output_dir):
    index, segment_data = segment
    try:
        dctx = zstd.ZstdDecompressor(dict_data=dictionary)
        decompressed_data = dctx.decompress(segment_data)

        output_file = os.path.join(output_dir, f'{index:08d}.dat')
        with open(output_file, 'wb') as out_file:
            out_file.write(decompressed_data)

        return f"Decompressed {index}.DAT, saved to {output_file}"
    except Exception as e:
        return f"Error decompressing {index}.dat: {e}"

# Function to extract and save the original segment
def extract_segment(pak_file, segment_index, magic_number):
    with open(pak_file, 'rb') as f:
        data = f.read()

    split_indices = []
    start = 0
    while (start := data.find(magic_number, start)) != -1:
        split_indices.append(start)
        start += len(magic_number)
    split_indices.append(len(data))  # Add EOF

    if segment_index < 1 or segment_index > len(split_indices) - 1:
        raise IndexError(f"out of range.")#Segment index {segment_index} is out of range.

    segment_start = split_indices[segment_index - 1]
    segment_end = split_indices[segment_index]

    return segment_start, segment_end, data[segment_start:segment_end]

# Function to compress the file
def compress_file(input_file, dict_data, compression_level):
    dictionary = zstd.ZstdCompressionDict(dict_data)
    cctx = zstd.ZstdCompressor(dict_data=dictionary, level=compression_level)

    with open(input_file, 'rb') as f:
        input_data = f.read()

    return cctx.compress(input_data)

# Function to replace the segment in the `.pak` file
def replace_segment(pak_file, segment_start, segment_end, compressed_data):
    original_segment_size = segment_end - segment_start

    if len(compressed_data) > original_segment_size:
        raise ValueError(
            f"Compressed data size ({len(compressed_data)} bytes) exceeds original size ({original_segment_size} bytes)."
        )

    with open(pak_file, 'rb+') as f:
        f.seek(segment_start)
        f.write(compressed_data)
        if len(compressed_data) < original_segment_size:
            f.write(b'\x00' * (original_segment_size - len(compressed_data)))

# Function to unpack the ZSDIC PAK

def unpack_zsdic():
    if not os.path.exists(ORIGINAL_ZSDIC_PAK):
        print("File does not exist. Please unpack the OBB file first, then click on Load ZSDIC PAK.")
        time.sleep(0.3)  # Pause for 0.3 seconds
        main()  # Call the main function after the delay
        return

    os.makedirs(UNPACK_DIR, exist_ok=True)
    with open(ORIGINAL_ZSDIC_PAK, 'rb') as f:
        data = f.read()

    dict_data = extract_dictionary(ORIGINAL_ZSDIC_PAK, DICT_START_HEX)
    dictionary = zstd.ZstdCompressionDict(dict_data)

    segments = split_segments(data, MAGIC_NUMBER)
    print(f"Starting to unpack {len(segments)} dat files.\nDO NOT CLOSE\nSearching for QuickBMS Script.bms")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(lambda s: decompress_segment(s, dictionary, UNPACK_DIR), segments)

    for result in results:
        print(result)

    # After repack, display a message and go to main
    print("Repacking complete. Returning to main menu...")
    time.sleep(0.3)  # Pause for 0.3 seconds
    main()


# Function to repack the ZSDIC PAK
def repack_zsdic():
    os.makedirs(REPACKED_DIR, exist_ok=True)
    try:
        if not os.path.exists(ORIGINAL_ZSDIC_PAK):
            raise FileNotFoundError("Original ZSDIC PAK not found!")
    except FileNotFoundError as e:
        print(e)
        time.sleep(0.5)
        main()

# Ensure main() executes regardless of the exception



    os.system(f"cp {ORIGINAL_ZSDIC_PAK} {REPACKED_PAK}")
    dict_data = extract_dictionary(ORIGINAL_ZSDIC_PAK, DICT_START_HEX)

    for file_name in os.listdir(EDITED_DAT_DIR):
        if file_name.endswith('.dat'):
            try:
                sequence_number = int(file_name.split('.')[0])
                input_file = os.path.join(EDITED_DAT_DIR, file_name)

                segment_start, segment_end, _ = extract_segment(REPACKED_PAK, sequence_number, MAGIC_NUMBER)

                for compression_level in range(1, MAX_COMPRESSION_LEVEL + 1):
                    try:
                        compressed_data = compress_file(input_file, dict_data, compression_level)
                        replace_segment(REPACKED_PAK, segment_start, segment_end, compressed_data)
                        print(f"Successfully reimported {file_name}")
                        time.sleep(0.4)
                        main()
                        break
                    except ValueError:
                        print(f"Error in reimporting trying again {compression_level}")
                        continue
                else:
                    print(f"Failed to reimport {file_name}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

def execute_script(script_path):
    if os.path.isfile(script_path):
        os.chmod(script_path, 0o777)
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
    else:
        print(f"{Colors.RED}{script_path} does not exist.{Colors.NOCOLOR}")

# Main function
def main():
    quickprint = """\
Custome QuickBMS generic files extractor and reimporter 1.2.3.#
by @HRModster
web:    Telegram
quickbms.com  Homepage
Telegram      @HRModster
THIS TOOL IS NOT FOR SALE

Options:
1. Unpack ZSDIC PAK
2. Repack ZSDIC PAK
3. LOAD ZSDIC PAK
4. move repacked ZSDIC PAK
5. Clear Unpacked ZSDIC
6. Search in ZSDIC
7. Back to Main menu
"""
    print(quickprint)

    choice = input("Enter your choice : ").strip()

    if choice == '1':
        unpack_zsdic()
    elif choice == '2':
        repack_zsdic()
    elif choice == '3':
        Load_pak()
    elif choice == '4':
        Move_pak()
    elif choice == '5':
        shutil.rmtree("/data/data/com.termux/files/home/Tool/obb/unpack_zsdic_pak")
    elif choice == '6':
        sscript_path1 = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T20"
        execute_script(sscript_path1)
        
    elif choice == '7':
        sscript_path = "/data/data/com.termux/files/home/Tool/HRModster_EXES/HRModster_T1"
        execute_script(sscript_path)
    else:
        print("Invalid choice.")
        time.sleep(0.2)
        main()

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
        sys.exit(1)
    main()