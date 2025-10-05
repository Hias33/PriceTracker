import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class AmazonScraper:
    def __init__(self):
        self.driver_path = "/usr/bin/chromedriver"  # Path to Chromedriver in container

    def get_driver(self):
        options = Options()
        options.add_argument("--headless")  # Headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def get_price(self, url: str) -> float | None:
        driver = self.get_driver()
        try:
            driver.get(url)
            time.sleep(5)  # wait for page to load

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Amazon price selectors
            price_tag = (
                soup.find("span", {"id": "priceblock_ourprice"}) or
                soup.find("span", {"id": "priceblock_dealprice"}) or
                soup.find("span", {"class": "a-price-whole"})
            )

            if not price_tag:
                logging.warning("No price tag found. Adjust the selector!")
                return None

            price_text = price_tag.get_text(strip=True).replace("€", "").replace(",", ".")
            try:
                return float(price_text)
            except ValueError:
                logging.error(f"Could not convert price to float: {price_text}")
                return None

        finally:
            driver.quit()
