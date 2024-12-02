from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Marketplace Scraper API. More features coming soon!"}

@app.get("/crawl_facebook_marketplace")
def crawl_facebook_marketplace(city: str, query: str, max_price: int):
    cities = {
        'New York': 'nyc',
        'Los Angeles': 'la',
        'Chicago': 'chicago',
        'Houston': 'houston'
    }
    if city in cities:
        city = cities[city]
    else:
        raise HTTPException(status_code=404, detail=f"{city} is not supported.")

    marketplace_url = f'https://www.facebook.com/marketplace/{city}/search/?query={query}&maxPrice={max_price}'
    initial_url = "https://www.facebook.com/login/device-based/regular/login/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(initial_url)
        time.sleep(2)
        # Login and scraping logic placeholder
        page.goto(marketplace_url)
        time.sleep(2)
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.find_all('div', class_='listing_class_placeholder')
        results = []
        for listing in listings:
            try:
                title = listing.find('span', 'title_class').text
                price = listing.find('span', 'price_class').text
                results.append({'title': title, 'price': price})
            except Exception:
                pass
        browser.close()
        return results
