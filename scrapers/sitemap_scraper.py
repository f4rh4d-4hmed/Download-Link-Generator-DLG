import requests
from bs4 import BeautifulSoup

def scrape_sitemap(base_url):
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'xml')
            links = soup.find_all('loc')
            with open("fitgirl_site.lock", "w") as f:
                for link in links:
                    f.write(link.text + '\n')
            print("Sitemap scraped successfully and links saved to fitgirl_site.lock.")
        else:
            print("Failed to retrieve sitemap. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

def main():
    while True:
        base_url = input("Enter the base URL of the XML sitemap (e.g., https://fitgirl-repacks.site/sitemap.xml): ")
        scrape_sitemap(base_url)
        choice = input("Do you want to scrape another sitemap? (yes/no): ").lower()
        if choice != 'y':
            break

if __name__ == "__main__":
    main()
