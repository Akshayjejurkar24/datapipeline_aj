# modules/db.py

from pymongo import MongoClient
from datetime import datetime
# DB setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "local"
COLLECTION_NAME = "Newscrappeddata"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

raw_collection = db["RawURLs"]
cleaned_collection = db["CleanedURLs"]
output_collection = db["firecrawldata"]
pdf_book_collection = db["PdfBookLinks"]
youtube_collection = db["YouTubeLinks"]


def insert_raw_urls(urls):
    for url in urls:
        if not raw_collection.find_one({"url": url}):
            raw_collection.insert_one({"url": url})

def insert_clean_urls(urls):
    for url in urls:
        if not cleaned_collection.find_one({"url": url}):
            cleaned_collection.insert_one({"url": url, "scraped": False})


def is_url_cleaned(url):
    return cleaned_collection.find_one({"url": url}) is not None

# save data in the applications
def insert_pdf_book_url(url, reason="pdf_or_book"):
    if not pdf_book_collection.find_one({"url": url}):
        pdf_book_collection.insert_one({
            "url": url,
            "reason": reason,
            "timestamp": datetime.utcnow() })



def insert_youtube_url(url, reason="youtube_link"):
    if not youtube_collection.find_one({"url": url}):
        youtube_collection.insert_one({
            "url": url,
            "reason": reason,
            "timestamp": datetime.utcnow()})