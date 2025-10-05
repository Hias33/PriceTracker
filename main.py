import json
import schedule
import time
import logging
from scraper.amazon_scraper import AmazonScraper
from notifier.discord_notifier import DiscordNotifier
from database.postgres import DatabaseHandler

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

# ---------- Config ----------
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

URL = config["url"]
WEBHOOK_URL = config["webhook_url"]
INTERVAL = config["check_interval_minutes"]
PRODUCT_NAME = config.get("product_name", "Amazon Product")

# ---------- Initialize objects ----------
scraper = AmazonScraper()
notifier = DiscordNotifier(WEBHOOK_URL)
db_handler = DatabaseHandler()  # Uses RaspberryPiDB, Prices, user: matthias, pwd: 1234

# ---------- Main logic ----------
def check_price():
    logging.info("Checking price...")
    current_price = scraper.get_price(URL)
    if current_price is None:
        logging.warning("Could not retrieve price.")
        return

    last_price = db_handler.load_last_price(URL)
    if last_price is None:
        logging.info(f"No previous price found. Setting to {current_price}€.")
        db_handler.save_price(PRODUCT_NAME, URL, current_price)
        return

    if current_price != last_price:
        logging.info(f"Price changed! Old: {last_price}€, New: {current_price}€")
        message = f"💸 Price change detected!\n{PRODUCT_NAME}\nNew price: **{current_price} €**\n{URL}"
        notifier.send_alert(message)
        db_handler.save_price(PRODUCT_NAME, URL, current_price)
    else:
        logging.info(f"No change ({current_price}€).")
        message = f"💸 Price change detected!\n{PRODUCT_NAME}\nNew price: **{current_price} €**\n{URL}"
        notifier.send_alert(message)

# ---------- Scheduler ----------
schedule.every(INTERVAL).minutes.do(check_price)
logging.info(f"Starting Price Tracker. Checking every {INTERVAL} minutes.")
check_price()  # initial check

while True:
    schedule.run_pending()
    time.sleep(5)
