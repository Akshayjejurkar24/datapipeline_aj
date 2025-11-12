# modules/scraper_launcher.py

from firecrawl import FirecrawlApp
from modules.data_processor import DataProcessor, extract_markdown_sections
from modules.config import FIRECRAWL_API_KEY
from modules.db import cleaned_collection, output_collection
from datetime import datetime





def run_scraper():
    urls_to_scrape = [doc["url"] for doc in cleaned_collection.find({"scraped": {"$ne": True}})]

    if not urls_to_scrape:
        print("ℹ️ No new URLs to scrape.")
        return

    print(f"🚀 Batch scraping {len(urls_to_scrape)} URLs...")

    firecrawl_app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    try:
        result = firecrawl_app.batch_scrape_urls(
            urls=urls_to_scrape,
            formats=["markdown"]
        )
        # print(result)
    except Exception as e:
        print(f"❌ Batch scrape failed: {e}")
        return

    for i, page in enumerate(result.data or []):
        try:
            # ✅ FirecrawlDocument object attribute access
            markdown = page.markdown
            metadata = page.metadata  # ❌ Don't use .dict() here
            url = metadata.get("sourceURL") or urls_to_scrape[i]
            processor = DataProcessor()
            main_clean = processor.extract_main_content(markdown)
            sections = extract_markdown_sections(main_clean)

            output_collection.insert_one({
                "url": url,
                "markdown": markdown,
                "main_clean_content": main_clean,
                "metadata": metadata,
                "main_data": sections,
                "timestamp": datetime.utcnow()
            })

            cleaned_collection.update_one({"url": url}, {"$set": {"scraped": True}})
            print(f"✅ Scraped & saved: {url}")

        except Exception as e:
            print(f"❌ Error processing result for URL index {i}: {e}")