# main_pipeline.py

from modules.url_collector import fetch_results
from modules.url_cleaner import clean_urls
from modules.scraper_launcher import run_scraper

QUERIES = [
"andy raskin strategic narrative case studies",
"common challenges with andy raskin strategic narrative",
"tools to improve andy raskin strategic narrative",
"andy raskin strategic narrative best practices",
"example of gtm experts on linkedin value proposition posts",
"gtm experts on linkedin value proposition posts case studies",
"common challenges with gtm experts on linkedin value proposition posts",
"tools to improve gtm experts on linkedin value proposition posts",
"gtm experts on linkedin value proposition posts best practices",
"example of mckinsey value proposition research pdf",
"mckinsey value proposition research pdf case studies",
"common challenges with mckinsey value proposition research pdf",
"tools to improve mckinsey value proposition research pdf",
"mckinsey value proposition research pdf best practices",
"example of forrester b2b buyer value insights 2025",
"forrester b2b buyer value insights 2025 case studies",

]

# for query in QUERIES:
#     print(f"\n🔍 Searching: {query}")
#     raw = fetch_results(query)
#     clean_urls(raw)  # Filtering + saving to CleanedURLs
# # ✅ Automatically scrape new URLs
# run_scraper()

total_scrape_ready = []
for query in QUERIES:
    print(f"\n🔍 Searching: {query}")
    raw = fetch_results(query)
    print(f"🔗 Fetched {len(raw)} URLs")
    cleaned = clean_urls(raw)
    print(f"✅ Cleaned & unique: {len(cleaned)} URLs")
    total_scrape_ready.extend(cleaned)
# ✅ Automatically scrape new URLs
if total_scrape_ready:
    print(f"\n🚀 Starting scrape for {len(total_scrape_ready)} new URLs...")
    run_scraper()
else:
    print("\nℹ️ No new URLs found for scraping.")