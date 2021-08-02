from scrapers.ipo_scraper_v2 import IPOScraperv2
from tasks.update_redis_hash import update_redis_hash
from core.constants import REDIS_HASHES


def fetch_and_store_v2():
    update_redis_hash(REDIS_HASHES['ipo_details_v2'])
    IPOScraperv2.ipo_scraper()
    print('✅ Fetch and store completed successfully')
    return
