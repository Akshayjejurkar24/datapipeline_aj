# serp_collector.py

import os
import time
import requests
from datetime import datetime
from modules.config import SERP_API_KEY
from modules.db import insert_raw_urls

# queries = ["strategy GTM goals and metrics"]
search_engine = "google"
MAX_RESULTS_PER_QUERY = 30



def fetch_results(query):
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERP_API_KEY,
        "num": MAX_RESULTS_PER_QUERY,  # e.g., 50
        "gl": "us",
        "hl": "en"
    }

    r = requests.get("https://serpapi.com/search.json", params=params)
    urls = []

    if r.status_code == 200:
        data = r.json()
        urls = [result["link"] for result in data.get("organic_results", [])]

    urls = list(set(urls))  # Remove duplicates
    insert_raw_urls(urls)
    return urls
