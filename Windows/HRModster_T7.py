import os
import shutil
import time
import subprocess
class Colors:
    NOCOLOR = '\033[0m'
    DARKGRAY = '\033[1;30m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
def set_permissions(file_path):
    """Set file permissions to 777 (read, write, and execute for everyone)."""
    try:
        os.chmod(file_path, 0o777)
    except PermissionError as e:
        print(f"Permission error setting permissions for {file_path}: {e}")
        time.sleep(2)  # Pause for 2 seconds to allow error reading
        raise

def get_single_file(directory, extension=None):
    """Find a single file in the directory. Optionally filter by file extension."""
    if extension:
        files = [f for f in os.listdir(directory) if f.endswith(extension)]
    else:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if len(files) == 0:
        raise FileNotFoundError(f"No files found in {directory}")
    if len(files) > 1:
        raise ValueError(f"Multiple files found in {directory}. Please delete all but one.")
    return os.path.join(directory, files[0])

def update_zip_file(zip_file_path):
    """Run the zip command to update the file in place after changing the directory."""
    zip_dir = os.path.dirname(zip_file_path)
    zip_file = os.path.basename(zip_file_path)

    # Set permissions before working with the file
    set_permissions(zip_file_path)

    os.chdir(zip_dir)

    try:
        subprocess.run(['zip', '-u', '-0', zip_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error updating file: {e}")
        time.sleep(2)  # Pause for 2 seconds to allow error reading
        raise

def adjust_size(repacked_obb_path, original_obb_size):
    """Adjust the size of repacked_obb by appending 00 bytes if it's smaller than original_obb."""
    repacked_obb_size = os.path.getsize(repacked_obb_path)

    if repacked_obb_size > original_obb_size:
        print("Error: repacked_obb is larger than original_obb. Please repackage and try again.")
        time.sleep(2)  # Pause for 2 seconds to allow error reading
        raise ValueError("Repacked OBB is larger than the original OBB.")

    with open(repacked_obb_path, 'ab') as repacked_obb_file:
        #print(f"Current size of repacked OBB: {repacked_obb_size} bytes")
        while repacked_obb_size < original_obb_size:
            # Add null byte (00) to the end of the file
            repacked_obb_file.write(b'\x00')
            repacked_obb_size += 1

    #print(f"Repacked OBB size adjusted to match original OBB size: {original_obb_size} bytes.")

def move_and_replace(src, dest):
    """Move the file to the destination. If the file exists at the destination, replace it."""
    if os.path.exists(dest):
        print(f"File {dest} already exists. Replacing it.")
        os.remove(dest)  # Remove the existing file
    shutil.move(src, dest)
    print(f"Moved file {src} to {dest}.")

def main():
    cwd = os.getcwd().split('/Tool')[0]
    unpacked_obb_dir = f"{cwd}/Tool/obb/unpacked_obb"
    repacked_obb_dir = f"{cwd}/Tool/obb/repacked_obb"
    original_obb_dir = f"{cwd}/Tool/obb/Original_obb"

    # Step 1: Find the .zip file in unpacked_obb
    zip_file_path = get_single_file(unpacked_obb_dir, extension='.zip')

    # Step 2: Run the zip command to update it
    update_zip_file(zip_file_path)

    # Step 3: Move the updated .zip file to repacked_obb, replacing if necessary
    repacked_obb_path = os.path.join(repacked_obb_dir, os.path.basename(zip_file_path))
    move_and_replace(zip_file_path, repacked_obb_path)

    # Step 4: Get the path of the original OBB file
    original_obb_path = get_single_file(original_obb_dir, extension='.obb')

    # Step 5: Get the size of the original OBB file
    original_obb_size = os.path.getsize(original_obb_path)
    #print(f"Original OBB size: {original_obb_size} bytes")
    time.sleep(2)  # Pause for 2 seconds to allow reading important size info

    # Step 6: Adjust the size of the repacked OBB file
    adjust_size(repacked_obb_path, original_obb_size)

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
    main()