import json
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from core.constants import URL, USER_AGENT_LIST, REDIS_HASHES
from redis_conf import RedisConf


class IPOScraper:
    @staticmethod
    def get_request_headers():
        return {
            'User-Agent': random.choice(USER_AGENT_LIST)
        }

    @staticmethod
    def ipo_scraper():
        header = IPOScraper.get_request_headers()
        page = requests.get(URL, header)
        soup = BeautifulSoup(page.text, 'html.parser')
        html_table = soup.find('table', {
            'class': 'table table-condensed table-bordered table-striped table-nonfluid table-hover'})
        data = IPOScraper.table_data_text(html_table)
        IPOScraper.store_in_redis(data[2:])

    @staticmethod
    def table_data_text(table):
    
        def row_get_data_text(tr, col_tag='td'): # td (data) or th (header)
            return [td.get_text(strip=True) for td in tr.find_all(col_tag)]
        rows = []
        trs = table.find_all('tr')
        header_row = row_get_data_text(trs[0], 'th')
        if header_row:  # if there is a header row include first
            rows.append(header_row)
            trs = trs[1:]
        for tr in trs: # for every table row
            rows.append(row_get_data_text(tr, 'td'))  # data row
        return rows
        list_table = table_data_text(htmltable)

    @staticmethod
    def store_in_redis(data):
        today = datetime.today()
        redis_client = RedisConf.create_connection_to_redis_server(True)
        for row in data:
            values_dict = {
                'Issuer Company': row[0],
                'Exchange': row[1],
                'Open': row[2],
                'Close': row[3],
                'Lot Size': row[4],
                'Issue Price (Rs)': row[5],
                'Issue Price (Rs. Cr.)': row[6]
            }
            try:
                ipo_closing_date = datetime.strptime(row[3], '%b %d, %Y')
            except Exception as e:
                print('❌ Invalid date format: ', e)
                return
            if ipo_closing_date > today:
                hash_name = REDIS_HASHES['current_ipo_details']
            else:
                hash_name = REDIS_HASHES['closed_ipo_details']
            value_json = json.dumps(values_dict)
            key = row[0]
            RedisConf.store_in_redis(
                r_client=redis_client,
                hash_name=hash_name,
                key=key,
                value=value_json
            )