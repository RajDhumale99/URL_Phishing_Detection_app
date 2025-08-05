import requests  # Better than aliasing it to re
from bs4 import BeautifulSoup
import os
import time  # For polite scraping

# Base test URL
URL = "https://www.kaggle.com"

# Initial request
try:
    response = requests.get(URL)
    print(f"Response --> {response} \ntype --> {type(response)}")
    print("status_code -->", response.status_code)

    if response.status_code != 200:
        print("HTTP connection is not successful! Try again.")
    else:
        print("HTTP connection is successful!")

    # Parse HTML
    soup = BeautifulSoup(response.content, "html.parser")
    print("Title with tags -->", soup.title, "\nTitle without tags -->", soup.title.text)

    # Print all link tags
    for link in soup.find_all("link"):
        print(link.get("href"))

    print(soup.get_text())

except Exception as e:
    print("An error occurred:", e)

# Step 1: Create folder
folder = "mini_dataset"
if not os.path.exists(folder):
    os.mkdir(folder)

# Step 2: Function to scrape URL content
def scrape_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("HTTP connection successful! for the URL:", url)
            return response
        else:
            print(f"Failed ({response.status_code}) for URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        print("Request error for URL:", url, "\nError:", e)
        return None

# Step 3: Save HTML to disk (fixing Unicode error)
path = os.path.join(os.getcwd(), folder)

def save_html(to_where, text, name):
    file_name = name + ".html"
    file_path = os.path.join(to_where, file_name)
    with open(file_path, "w", encoding="utf-8") as f:  # Specify UTF-8 encoding
        f.write(text)

# Step 4: List of URLs
URL_list = [
    "https://www.python.org",
    "https://stackoverflow.com",
    "https://realpython.com",
    "https://www.github.com",
    "https://scholar.google.com",
    "https://www.w3schools.com",
    "https://www.khanacademy.org",
    "https://pubmed.ncbi.nlm.nih.gov",
    "https://data.gov.in",
    "https://www.bbc.com"
]

# Step 5: Create dataset from list
def create_mini_dataset(to_where, url_list):
    for i, url in enumerate(url_list):
        content = scrape_content(url)
        if content is not None:
            save_html(to_where, content.text, str(i))
        time.sleep(1)  # Polite delay between requests
    print("Mini dataset created successfully!")

# Step 6: Call to create the dataset
create_mini_dataset(path, URL_list)