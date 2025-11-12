# modules/url_cleaner.py

from urllib.parse import urlparse
from modules.data_processor import EXCLUDED_DOMAINS

from modules.db import is_url_cleaned, insert_clean_urls, insert_pdf_book_url, insert_youtube_url

def get_domain(url):
    try:
        domain = urlparse(url).netloc.lower()
        return domain[4:] if domain.startswith("www.") else domain
    except:
        return ""
    

def is_pdf_or_book(url):
    url_lower = url.lower()
    return (
        url_lower.endswith(".pdf")
        or "books.google." in url_lower
        or "amazon." in url_lower and "/dp/" in url_lower  # common book pattern
        or "book" in url_lower and ("preview" in url_lower or "read" in url_lower)
    )

# you tube link
def is_youtube_url(url):
    domain = get_domain(url)
    return "youtube.com" in domain or "youtu.be" in domain
def clean_urls(new_urls):

    cleaned = []
    for url in set(new_urls):
        domain = get_domain(url)

        if any(bad in domain for bad in EXCLUDED_DOMAINS):
            print(f"🚫 Domain excluded: {domain}")
            continue

        if is_url_cleaned(url):
            print(f"🔁 Already cleaned: {url}")
            continue

        if is_pdf_or_book(url):
            print(f"📄 PDF/book detected: {url}")
            insert_pdf_book_url(url)
            continue
        
        if is_youtube_url(url):
            print(f"📹 YouTube link detected: {url}")
            insert_youtube_url(url)
            continue

        cleaned.append(url)

    insert_clean_urls(cleaned)
    return cleaned

# url_cleaner.py
