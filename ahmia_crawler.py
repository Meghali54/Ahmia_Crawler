import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import logging
import sys
import re
import os

# === MongoDB Configuration ===
MONGO_URI = os.environ.get("MONGO_URI")  # Secret should be set in GitHub/Render
DB_NAME = "onion_monitor"
COLLECTION_NAME = "ahmia_links"

# === Logging Configuration ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# === Fetch Links from Ahmia ===
def fetch_ahmia_links():
    try:
        logging.info("Fetching from Ahmia...")
        response = requests.get("https://ahmia.fi/onions/", timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        all_text = soup.get_text()
        links = set(re.findall(r"http[s]?://[a-zA-Z2-7]{16,56}\.onion", all_text))
        logging.info(f"Fetched {len(links)} links from Ahmia.")
        return links
    except Exception as e:
        logging.error(f"Error fetching Ahmia links: {e}")
        return set()

# === Save New Links Only ===
def save_new_links(links):
    try:
        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set.")

        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        existing_links = set(
            doc["onionLink"]
            for doc in collection.find({"source": "Ahmia"}, {"onionLink": 1})
        )
        new_links = links - existing_links
        timestamp = datetime.utcnow().isoformat()
        docs = [
            {"onionLink": link, "source": "Ahmia", "crawledTimestamp": timestamp}
            for link in new_links
        ]
        if docs:
            collection.insert_many(docs)
            logging.info(f"Inserted {len(docs)} new links.")
        else:
            logging.info("No new links found.")
    except Exception as e:
        logging.error(f"MongoDB error: {e}")

# === Run Once ===
def run():
    logging.info("=== Ahmia Crawler Started ===")
    links = fetch_ahmia_links()
    if links:
        save_new_links(links)
    logging.info("=== Ahmia Crawler Finished ===\n")

if __name__ == "__main__":
    run()
