from scrapers.ipo_scraper import IPOScraper


def fetch_and_store():
    IPOScraper.ipo_scraper()
    print('✅ Fetch and store completed successfully')
    return
