import requests
from bs4 import BeautifulSoup
import os

PAGES = {
    "home": "https://www.aiet.org.in/",
    "about": "https://www.aiet.org.in/about",
    "departments": "https://www.aiet.org.in/departments",
    "admissions": "https://www.aiet.org.in/admissions",
    "placements": "https://www.aiet.org.in/placements",
    "facilities": "https://www.aiet.org.in/facilities",
    "contact": "https://www.aiet.org.in/contact",
}

os.makedirs("data/scraped", exist_ok=True)

def scrape_page(name, url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        with open(f"data/scraped/{name}.txt", "w", encoding="utf-8") as f:
            f.write(f"Source: {url}\n\n{text}")
        print(f"✅ Scraped: {name}")
    except Exception as e:
        print(f"❌ Failed {name}: {e}")

if __name__ == "__main__":
    for name, url in PAGES.items():
        scrape_page(name, url)
    print("\n✅ All pages scraped and saved to data/scraped/")
