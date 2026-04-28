import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

# ── Config ─────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Target: books.toscrape.com (a free, legal practice site)
BASE_URL = "https://books.toscrape.com/catalogue/"


# ── Scrape a single page ───────────────────────────────────
def scrape_page(url):
    """
    Scrapes one page of books.toscrape.com.
    Returns a list of dicts with title, price, rating, availability.
    """
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch {url} — status {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    results = []
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    for book in books:
        title  = book.h3.a["title"]
        price  = book.find("p", class_="price_color").text.strip()
        avail  = book.find("p", class_="instock availability").text.strip()
        rating = book.p["class"][1]   # e.g. "Three"

        results.append({
            "title"       : title,
            "price"       : float(price.replace("£", "").replace("Â", "")),
            "rating"      : rating_map.get(rating, 0),
            "availability": avail,
            "scraped_at"  : datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    return results


# ── Scrape multiple pages ──────────────────────────────────
def scrape_catalogue(max_pages=3):
    """
    Scrapes up to max_pages pages from the catalogue.
    Adds a 1-second delay between requests (polite scraping).
    """
    all_books = []

    for page_num in range(1, max_pages + 1):
        url = f"{BASE_URL}page-{page_num}.html"
        print(f"Scraping page {page_num}...")

        books = scrape_page(url)
        all_books.extend(books)

        time.sleep(1)   # be polite — don't hammer the server

    return all_books


# ── Analyze with pandas ────────────────────────────────────
def analyze(df):
    print(f"\n{'='*50}")
    print(f"  Scrape summary — {len(df)} books found")
    print(f"{'='*50}")
    print(f"  Avg price    : £{df['price'].mean():.2f}")
    print(f"  Cheapest     : £{df['price'].min():.2f}")
    print(f"  Most expensive: £{df['price'].max():.2f}")
    print(f"  Avg rating   : {df['rating'].mean():.1f} / 5")
    print()

    print("  Top 5 cheapest books:")
    cheap = df.nsmallest(5, "price")[["title", "price", "rating"]]
    print(cheap.to_string(index=False))
    print()

    print("  Top 5 highest rated:")
    top = df[df["rating"] == 5].head(5)[["title", "price", "rating"]]
    print(top.to_string(index=False))


# ── Save results ───────────────────────────────────────────
def save(df, filename="books.csv"):
    df.to_csv(filename, index=False)
    print(f"\nData saved to {filename}")


# ── Main ───────────────────────────────────────────────────
if __name__ == "__main__":
    pages = int(input("How many pages to scrape? (1-50): "))
    pages = max(1, min(pages, 50))

    raw   = scrape_catalogue(max_pages=pages)
    df    = pd.DataFrame(raw)

    analyze(df)
    save(df)
