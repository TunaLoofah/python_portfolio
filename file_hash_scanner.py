import os
import hashlib
from prettytable import PrettyTable

def calculate_hashes(file_path):
    """Calculate MD5 and SHA-256 hashes of a file."""
    with open(file_path, "rb") as f:
        file_data = f.read()
        md5_hash = hashlib.md5(file_data).hexdigest()
        sha256_hash = hashlib.sha256(file_data).hexdigest()
    return md5_hash, sha256_hash

# Prompt the user to input a directory
directory = input("Enter the directory to scan: ").strip()
file_hashes = []  # List to store file information (MD5, SHA-256, File Path)

# Traverse the directory and its subdirectories
for root, _, files in os.walk(directory):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        try:
            md5_hash, sha256_hash = calculate_hashes(file_path)
            file_hashes.append((file_path, md5_hash, sha256_hash))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# Create and populate the PrettyTable
table = PrettyTable(["File Path", "MD5 Hash", "SHA-256 Hash"])
table.align = "l"
table.hrules = 1  # Add horizontal lines to separate rows
for file_path, md5_hash, sha256_hash in file_hashes:
    table.add_row([file_path, md5_hash, sha256_hash])

# Print the table
print("\n")
print(table)
print("\nEnd Script")

