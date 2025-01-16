import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag             # install nltk package averaged_perceptron_tagger, averaged_perceptron_tagger_eng, stopwords, punkt_tab
from prettytable import PrettyTable

BASE_URL = input("Enter the base URL to scrape: ").strip()

unique_urls = set()
image_links = set()
phone_numbers = set()
zip_codes = set()
text_content = ""

zipPatt = re.compile(r'\b\d{5}(?:-\d{4})?\b')
phonePatt = re.compile(r'\(?\d{3}\)?-? *\d{3}-? *-?\d{4}')

def scrape_page(url, visited):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"Scraping: {url}")

        for link in soup.find_all('a', href=True):
            full_url = urljoin(BASE_URL, link['href'])
            if full_url.startswith(BASE_URL) and full_url not in visited:
                visited.add(full_url)
                unique_urls.add(full_url)
                scrape_page(full_url, visited)

        for img in soup.find_all('img', src=True):
            img_url = urljoin(BASE_URL, img['src'])
            image_links.add(img_url)

        global text_content
        text_content += soup.get_text(separator=" ", strip=True)

        phone_numbers.update(phonePatt.findall(soup.get_text()))
        zip_codes.update(zipPatt.findall(soup.get_text()))
    except Exception as e:
        print(f"Error scraping {url}: {e}")

visited_pages = set()
print("Scraping in progress...")
scrape_page(BASE_URL, visited_pages)

tokens = word_tokenize(text_content.lower())
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

unique_vocabulary = set(filtered_tokens)

pos_tags = pos_tag(filtered_tokens)

verbs = {word for word, tag in pos_tags if tag.startswith('VB')}
nouns = {word for word, tag in pos_tags if tag.startswith('NN')}

print("\n===== Full Scraping Results =====\n")
print("Unique URLs Found:")
print("\n".join(unique_urls) + "\n")

print("Image Links Found:")
print("\n".join(image_links) + "\n")

print("Phone Numbers Found:")
print("\n".join(phone_numbers) + "\n")

print("Zip Codes Found:")
print("\n".join(zip_codes) + "\n")

print("Unique Vocabulary:")
print(", ".join(sorted(unique_vocabulary)) + "\n")

print("Verbs Identified:")
print(", ".join(sorted(verbs)) + "\n")

print("Nouns Identified:")
print(", ".join(sorted(nouns)) + "\n")


print("\n===== Generating Summary =====\n")
table = PrettyTable()
table.title = "Website Scraping Report"
table.field_names = ["Category", "Details"]

table.add_row(["Unique URLs", f"{len(unique_urls)} URLs found"])
table.add_row(["Image Links", f"{len(image_links)} images found"])
table.add_row(["Phone Numbers", f"{len(phone_numbers)} phone numbers found"])
table.add_row(["Zip Codes", f"{len(zip_codes)} zip codes found"])
table.add_row(["Unique Vocabulary", f"{len(unique_vocabulary)} unique words"])
table.add_row(["Verbs", f"{len(verbs)} verbs identified"])
table.add_row(["Nouns", f"{len(nouns)} nouns identified"])

print(table)

with open("URL_Scrape_Report.txt", "w") as f:
    f.write("===== Website Scraping Report =====\n\n")
    
    f.write("Unique URLs:\n")
    f.write("\n".join(unique_urls) + "\n\n")
    
    f.write("Image Links:\n")
    f.write("\n".join(image_links) + "\n\n")
    
    f.write("Phone Numbers:\n")
    f.write("\n".join(phone_numbers) + "\n\n")
    
    f.write("Zip Codes:\n")
    f.write("\n".join(zip_codes) + "\n\n")
    
    f.write("Unique Vocabulary:\n")
    f.write(", ".join(sorted(unique_vocabulary)) + "\n\n")
    
    f.write("Verbs:\n")
    f.write(", ".join(sorted(verbs)) + "\n\n")
    
    f.write("Nouns:\n")
    f.write(", ".join(sorted(nouns)) + "\n\n")

print("Report successfully saved to 'URL_Scrape_Report.txt'.")




