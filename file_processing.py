import os
import stat
import time
import hashlib

class FileProcessor:        # Define the FileProcessor class
    def __init__(self, filepath):           # Initializes the FileProcessor object collecting details: size, permissions (mode), timestamps, and user ID
        self.filepath = filepath
        try:
            file_stat = os.stat(filepath)
            self.filesize = os.path.getsize(filepath)
            self.mode = stat.filemode(file_stat.st_mode)
            self.modify_time = time.ctime(file_stat.st_mtime)
            self.access_time = time.ctime(file_stat.st_atime)
            self.create_time = time.ctime(file_stat.st_ctime)
            self.uid = file_stat.st_uid
            self.header = None
            self.md5_hash = None
        except FileNotFoundError:           # If the file is not found, print an error message and set filesize to None
            print(f"File '{filepath}' does not exist or cannot be accessed.")
            self.filesize = None
    
    def GetFileHeader(self):
        if self.filesize:                   # Only attempt if the file exists
            with open(self.filepath, 'rb') as f:
                self.header = f.read(20)            # Reads the first 20 bytes of the header
    
    def GetFileMD5Hash(self):           # Computes the MD5 hash of the file content
        if self.filesize:               # Only attempt if the file exists
            try:
                with open(self.filepath, 'rb') as fileToHash:
                    self.md5_hash = hashlib.md5(fileToHash.read()).hexdigest()
            except Exception as err:
                self.md5_hash = f"Error: {err}"
    
    def PrintFileDetails(self):             # Prints the details
        if self.filesize:
            print("\n" + "="*20 + "File Details".center(20) + "="*20)
            print(f"Path: {self.filepath}")
            print(f"Size: {self.filesize} bytes")
            print(f"Last Modified: {self.modify_time}")
            print(f"Last Accessed: {self.access_time}")
            print(f"Created: {self.create_time}")
            print(f"Mode: {self.mode}")
            print(f"UserID: {self.uid}")
            if self.header:
                print(f"Header: {self.header.hex()}")
            if self.md5_hash:
                print(f"MD5 Hash: {self.md5_hash}")
        else:
            print(f"File '{self.filepath}' was skipped (not found).")
        print("="*60)

directory_path = input("Enter the directory path: ")            # Prompts the user for the directory path

try:            # Try to access and process each file in the specified directory
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        try:
            file_processor = FileProcessor(filepath)
            file_processor.GetFileHeader()              # Gets file header
            file_processor.GetFileMD5Hash()             # Computes MD5 hash
            file_processor.PrintFileDetails()           # Prints details and hash
        except Exception as e:          # Error handling of the file processing and accessing the directory
            print(f"Error processing file '{filename}': {e}")
except Exception as e:
    print(f"Error accessing directory: {e}")
print("\nEnd Script")