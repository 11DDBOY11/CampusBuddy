import requests
from bs4 import BeautifulSoup
import os

PAGES = {
    "home": "https://new.aiet.org.in/",
    "about": "https://new.aiet.org.in/about/college",
    "vision_mission": "https://new.aiet.org.in/about/vision-mission",
    "academics_cse": "https://new.aiet.org.in/academics/cse",
    "academics_ai": "https://new.aiet.org.in/academics/ai",
    "academics_ise": "https://new.aiet.org.in/academics/ise",
    "academics_ece": "https://new.aiet.org.in/academics/ece",
    "admissions_kcet": "https://new.aiet.org.in/admissions/kcet",
    "admissions_comedk": "https://new.aiet.org.in/admissions/comedk",
    "research": "https://new.aiet.org.in/Research",
    "placements": "https://new.aiet.org.in/placement",
    "campus_life": "https://new.aiet.org.in/campus-life",
    "contact": "https://new.aiet.org.in/contact",
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
        print(f"Scraped: {name}")
    except Exception as e:
        print(f"Failed {name}: {e}")

if __name__ == "__main__":
    for name, url in PAGES.items():
        scrape_page(name, url)
    print("\nAll pages scraped and saved to data/scraped/")
