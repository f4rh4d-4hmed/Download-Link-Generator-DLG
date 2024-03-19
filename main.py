from colorama import init, Fore, Style
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Initialize Colorama
init(autoreset=True)

# Author signature
author_signature = Fore.YELLOW + Style.BRIGHT + """

▒█▀▀▀ ▀▀█▀▀ ▒█▀▀█ ░░ ▒█▀▀▄ ▒█▀▀▀█ ▒█░░▒█ ▒█▄░▒█ ▒█░░░ ▒█▀▀▀█ ░█▀▀█ ▒█▀▀▄ ▒█▀▀▀ ▒█▀▀█ 
▒█▀▀▀ ░▒█░░ ▒█▄▄█ ▀▀ ▒█░▒█ ▒█░░▒█ ▒█▒█▒█ ▒█▒█▒█ ▒█░░░ ▒█░░▒█ ▒█▄▄█ ▒█░▒█ ▒█▀▀▀ ▒█▄▄▀ 
▒█░░░ ░▒█░░ ▒█░░░ ░░ ▒█▄▄▀ ▒█▄▄▄█ ▒█▄▀▄█ ▒█░░▀█ ▒█▄▄█ ▒█▄▄▄█ ▒█░▒█ ▒█▄▄▀ ▒█▄▄▄ ▒█░▒█
"""
print(author_signature)

# Created By
print(Fore.CYAN + Style.BRIGHT + "Created By: Farhad Ahmed")

# Version
print(Fore.GREEN + Style.BRIGHT + "Version: 0.0.1")

# Set to keep track of visited URLs
visited_urls = set()

# Base URL of the website
base_url = 'http://103.170.204.250/FILE/'

# Function to scan a URL
def scan_url(url):
    # Check if URL has already been visited
    if url in visited_urls:
        return
    
    # Add URL to visited set
    visited_urls.add(url)
    
    # Fetch HTML content
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Search for specified file formats
        file_formats = ['.mp4', '.mkv', '.mp3', '.rar', '.zip', '.pkg', '.dod']
        for link in soup.find_all('a'):
            href = link.get('href')
            full_url = urljoin(url, href)  # Construct full URL
            
            if any(format in href for format in file_formats):
                # Save full URL to found.html
                with open('urls.txt', 'a') as file:
                    file.write(f"{full_url}\n")
            else:
                # Recursively explore directory links
                if href.endswith('/'):
                    scan_url(full_url)
    
    else:
        print(Fore.RED + f"Failed to fetch URL: {url}")

# Start scanning from the top URL
scan_url(base_url)

# Check if the entire website is scanned by comparing the number of visited URLs
# If the top URL is visited twice, stop the scanning process
if len(visited_urls) > 1:
    print(Fore.GREEN + "Scanning complete.")
