# Python Standard Libraries
import requests                         # Python Standard Library for URL requests
import os                               # For saving image files

# Python 3rd Party Libraries
from bs4 import BeautifulSoup           # 3rd Party BeautifulSoup Library - pip install beautifulsoup4
from prettytable import PrettyTable     # PrettyTable Library - pip install prettytable

# Input the URL dynamically
url = input("Enter the URL to scrape: ")

try:
    page = requests.get(url)            # Retrieve the web page
    page.raise_for_status()             # Check if the request was successful
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

soup = BeautifulSoup(page.text, 'html.parser')      # Create a BeautifulSoup object for processing

# Extract the page title
print("Page Title:")
if soup.title:
    print(soup.title.string)
else:
    print("No Title Found")
print("\n") 

# Extract and display all the links
print("Links found on the page:")
links = soup.find_all('a', href=True)           # Get all anchor tags with href attributes
link_table = PrettyTable()
link_table.field_names = ["Link URL"]
link_table.align = "l"  # Align columns to the left
for link in links:
    link_url = link['href']                     # Simply retrieve the URL as it appears
    if not link_url.startswith(('http', 'https')):  # Handle relative URLs
        link_url = url.rstrip('/') + '/' + link_url.lstrip('/')
    link_table.add_row([link_url])
print(link_table)
print("\n")  

# Extract and display images
print("Images found on the page:")
images = soup.find_all('img')                   # Find all image tags
image_table = PrettyTable()
image_table.field_names = ["Image URL", "Alt Text"]
image_table.align = "l"  # Align columns to the left
for img in images:
    try:
        img_url = img['src']
        if not img_url.startswith(('http', 'https')):  # Handle relative URLs
            img_url = url.rstrip('/') + '/' + img_url.lstrip('/')
        alt_text = img.get('alt', 'No Alt Text')       # Display the alt text
        
        image_table.add_row([img_url, alt_text])
        
        response = requests.get(img_url)                # Download the image
        response.raise_for_status()                    # Check if the request was successful
        image_name = os.path.basename(img_url)          # Save image with its base name
        with open(image_name, 'wb') as outFile:
            outFile.write(response.content)
    
    except Exception as err:
        print(f"Error fetching image {img_url}: {err}")
        continue                                        # Skip to the next image if there's an error
print(image_table)
print("\nScript Complete")
