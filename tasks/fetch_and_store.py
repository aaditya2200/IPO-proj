from scrapers.ipo_scraper import IPOScraper
from tasks.update_redis_hash import update_redis_hash
from core.constants import REDIS_HASHES


def fetch_and_store():
    update_redis_hash(REDIS_HASHES['current_ipo_details'])
    IPOScraper.ipo_scraper()
    print('✅ Fetch and store completed successfully')
    return
