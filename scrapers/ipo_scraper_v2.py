
import random
import requests
from bs4 import BeautifulSoup

from core.constants import USER_AGENT_LIST
#from redis_conf import RedisConf

URL = "https://investorzone.in/ipo/"

class IPOScraperv2:
    @staticmethod
    def get_request_headers():
        return {
            'User-Agent': random.choice(USER_AGENT_LIST)
        }

    @staticmethod
    def ipo_scraper():

        header = IPOScraperv2.get_request_headers()
        page = requests.get(URL, header)
        soup = BeautifulSoup(page.text, 'html.parser')
        html_table = soup.find('table', {
            'class': 'table-fill-1 table-fill font-setting'})
        data = IPOScraperv2.table_data_text(html_table)

        return(data[2:])

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
        
        

    
    







