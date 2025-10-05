# Raspberry Pi Price Tracker

A lightweight **Price Tracker for Amazon** built in Python, designed to run on a **Raspberry Pi 4 (ARM64)** using Docker.  
Tracks product prices, stores them in **PostgreSQL**, and sends **Discord notifications** when checking prices.

---

## Features

- Tracks Amazon product prices
- Stores price history in PostgreSQL
- Sends Discord notifications for price updates
- Fully Dockerized for Raspberry Pi 4 / ARM64
- Headless Chrome for efficient scraping

---

## Project Structure

```text
Price_Tracker/
├─ main.py
├─ config.json
├─ requirements.txt
├─ Dockerfile
├─ scraper/
│  └─ amazon_scraper.py
├─ notifier/
│  └─ discord_notifier.py
├─ database/
│  └─ postgres.py
