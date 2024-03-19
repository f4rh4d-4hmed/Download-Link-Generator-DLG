import os
import urllib.parse
import webbrowser
import requests
from colorama import init, Fore, Style

# Initialize Colorama
init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_urls(keyword):
    urls = []
    if os.path.exists('url.lock'):
        with open('url.lock', 'r') as file:
            for line in file:
                title_start = line.rfind('/') + 1
                title_end = line.rfind('.')
                title = line[title_start:title_end].lower()
                url = line.lower()
                keyword_words = keyword.lower().split()
                # Check if all words in the keyword are present in either the title or the URL
                if all(word in title or word in url for word in keyword_words):
                    urls.append(line.strip())
    return urls

def format_text(text):
    # Replace %20 with spaces, replace dots with spaces
    formatted_text = text.replace('%20', ' ')
    formatted_text = formatted_text.replace('.', ' ')
    return formatted_text

def format_file_name(url):
    # Decode URL and replace %20 with spaces, replace dots with spaces
    file_name = urllib.parse.unquote(url.split('/')[-1])
    file_name = file_name.replace('.', ' ')
    return file_name.rsplit('.', 1)[0]  # Remove file extension

def download_file(url):
    try:
        file_name = url.split('/')[-1]
        with open(file_name, 'wb') as f:
            response = requests.get(url)
            f.write(response.content)
        print(Fore.GREEN + f"File '{file_name}' downloaded successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred while downloading the file: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Opening the link in browser instead..." + Style.RESET_ALL)
        webbrowser.open(url)

def main():
    while True:
        clear_screen()  # Clear the screen before displaying new content
        if not os.path.exists('url.lock'):
            print(Fore.RED + "Error: 'url.lock' file not found." + Style.RESET_ALL)

        keyword = input(Fore.MAGENTA + "Author:Farhad Ahmed\nVersion:0.0.1\nEnter The Movie Or Animation Or Games Name: " + Style.RESET_ALL)

        matching_urls = search_urls(keyword)

        if matching_urls:
            print(Fore.CYAN + "Matching URLs:" + Style.RESET_ALL)
            for i, url in enumerate(matching_urls, 1):
                print(f"{i}. {format_file_name(url)}")
            
            selected_index = input(Fore.MAGENTA + "Here Is the results\nType the number from list: " + Style.RESET_ALL).strip()
            if selected_index.isdigit():
                index = int(selected_index) - 1
                if 0 <= index < len(matching_urls):
                    selected_url = matching_urls[index]
                    print(Fore.GREEN + f"Selected URL: {selected_url}" + Style.RESET_ALL)
                    while True:
                        option = input("\nSelect an option:\n1. Download\n2. Open in browser\n3. Show link\nEnter option number: ").strip()
                        if option == '1':
                            download_file(selected_url)
                            break
                        elif option == '2':
                            webbrowser.open(selected_url)
                            break
                        elif option == '3':
                            print(selected_url)
                            break
                        else:
                            print(Fore.RED + "Invalid option. Please enter a valid option number." + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Invalid index. Please enter a valid index." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid input. Please enter a number." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "No matching URLs found." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
