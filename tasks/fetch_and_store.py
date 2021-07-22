from scrapers.ipo_scraper import IPOScraper
from tasks.update_redis_hash import update_redis_hash


def fetch_and_store():
    update_redis_hash()
    IPOScraper.ipo_scraper()
    print('✅ Fetch and store completed successfully')
    return
