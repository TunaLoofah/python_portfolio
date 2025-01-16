import os                      
import sys                     
from datetime import datetime    
from PIL import Image       
from prettytable import PrettyTable

def analyze_image(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format, img.width, img.height, img.mode
    except Exception as e:
        return None, None, None, None

def process_directory(directory_path):
    resultTable = PrettyTable(['File', 'Ext', 'Format', 'Width', 'Height', 'Mode'])
    
    resultTable.align["File"] = "l"
    resultTable.align["Ext"] = "l"
    resultTable.align["Format"] = "l"
    resultTable.align["Width"] = "l"
    resultTable.align["Height"] = "l"
    resultTable.align["Mode"] = "l"
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower() 
            img_format, width, height, mode = analyze_image(file_path)
            if img_format: 
                resultTable.add_row([file_path, ext, img_format, width, height, mode])
            else:
                resultTable.add_row([file_path, ext, 'Not an image', '-', '-', '-'])

    print(resultTable)

if __name__ == "__main__":
    print("Image File Analyzer")
    print("Script Started", str(datetime.now())) 
    print()

    directory_path = input("Enter the path to the directory containing image files: ").strip()

    if not os.path.isdir(directory_path):
        print("Invalid directory path. Please try again.")
        sys.exit()

    process_directory(directory_path)
print("\nEnd Script")