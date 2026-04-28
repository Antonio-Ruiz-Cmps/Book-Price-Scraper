# Book Price Scraper

A Python web scraper that extracts book titles, prices,
ratings and availability from books.toscrape.com — a free,
legal site built for scraping practice.

## Features
- Scrapes 1 to 50 pages (up to 1,000 books)
- Extracts: title, price, star rating, availability
- Polite scraping with 1-second delay between requests
- Analyzes data with pandas (avg price, cheapest, top rated)
- Saves full results to CSV

## Tech stack
- Python 3.10+
- requests
- BeautifulSoup4
- pandas

## Setup

```bash
pip install requests beautifulsoup4 pandas
python main.py
```

## Example output

```
Scraping page 1...
Scraping page 2...
Scraping page 3...

Scrape summary — 60 books found
  Avg price     : £35.18
  Cheapest      : £10.00
  Most expensive: £59.69
  Avg rating    : 3.1 / 5
...
Data saved to books.csv
```

## Notes
- books.toscrape.com is a sandbox site made for practice
- No login or API key required
- Output CSV can be imported into Excel or Google Sheets

## What I learned
- How to send HTTP requests with custom headers
- How to parse HTML with BeautifulSoup
- How to clean and analyze scraped data with pandas
- How to implement polite scraping with time.sleep()

## Author
Antonio de Jesus Ruiz Campos — built as part of a Python portfolio.
