from colorama import init, Fore, Style
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import traceback
from datetime import datetime

init(autoreset=True)

author_signature = Fore.YELLOW + Style.BRIGHT + """
███████████████████████████████████████████
█─▄▄▄▄█─▄▄▄─█▄─▄▄▀██▀▄─██▄─▄▄─█▄─▄▄─█▄─▄▄▀█
█▄▄▄▄─█─███▀██─▄─▄██─▀─███─▄▄▄██─▄█▀██─▄─▄█
▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▄▄▀▄▄▀
"""
print(author_signature)

print(Fore.CYAN + Style.BRIGHT + "Created By: Farhad Ahmed")

print(Fore.GREEN + Style.BRIGHT + "Version: 0.0.2")

visited_urls = set()

def scan_url(url):
    try:

        if url in visited_urls:
            return
        
        visited_urls.add(url)
        
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            file_formats = ['.mp4', '.mkv', '.mp3', '.rar', '.zip', '.pkg', '.dod', '.exe', '.iso', '.jar', '.pdf', '.bat', '.torrent']
            for link in soup.find_all('a'):
                href = link.get('href')
                full_url = urljoin(url, href)
                
                if any(format in href for format in file_formats):
                    with open('urls.txt', 'a') as file:
                        file.write(f"{full_url}\n")
                else:
                    if href.endswith('/'):
                        scan_url(full_url)
        
        else:
            print(Fore.RED + f"Failed to fetch URL: {url}")
    
    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        crash_report_filename = f"crash_report_{timestamp}.txt"
        with open(crash_report_filename, 'w') as file:
            file.write(f"Crash report generated at: {timestamp}\n")
            file.write(f"URL causing crash: {url}\n\n")
            file.write("Traceback:\n")
            traceback.print_exc(file=file)

            print(Fore.RED + f"An error occurred while scanning URL: {url}. Crash report generated: {crash_report_filename}")

base_url = input("Enter the base URL of the website to scan: ")

start_time = datetime.now()
print(Fore.CYAN + f"Scanning started at: {start_time}")

scan_url(base_url)

end_time = datetime.now()
print(Fore.CYAN + f"Scanning completed at: {end_time}")

if len(visited_urls) > 1:
    print(Fore.GREEN + "Scanning complete.")
