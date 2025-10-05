import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseHandler:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        self.cursor = self.conn.cursor()

    def save_price(self, product_name, url, price):
        self.cursor.execute(
            "INSERT INTO prices (product_name, url, price, checked_at) VALUES (%s, %s, %s, %s)",
            (product_name, url, price, datetime.now())
        )
        self.conn.commit()

    def load_last_price(self, url):
        self.cursor.execute(
            "SELECT price FROM prices WHERE url=%s ORDER BY checked_at DESC LIMIT 1",
            (url,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
