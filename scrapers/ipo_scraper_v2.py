
import random
import requests
import re
from bs4 import BeautifulSoup


from core.constants import USER_AGENT_LIST,REDIS_HASHES
from redis_conf import RedisConf

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
        #we can write logic so that it only takes current and future IPO for reddis as we dont really need older ones? idk
        IPOScraperv2.store_in_redis(data[2:])

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
        
    
    ## LOGIC for going through comapny names and running RHP_scraper will come here.
    #===========================================================================#
    def scrapeRHP():
        
    
    @staticmethod
    def RHP_scraper(companyName):
        # Right now only printing string of RHP url #saving document feasibility not studied yet
        companyName = companyName.replace(" ","-")
        DRHP_URL = "https://investorzone.in/ipo/" + companyName +"/"
        page = requests.get(URL, header)
        soup = BeautifulSoup(page.text, 'html.parser')

        buttons = soup,findAll('div',{'class' : 'button-link'})

        #link = soup.find('a' ,{'href': 'https://d2un9pqbzgw43g.cloudfront.net/main/*drhp.pdf'})

        #there are two link one for draft RHP and another for RHP to access RHP just go for second item in array , some companies wont have RHP ready thats why i kept this array.
        links =[]

        for b in buttons:
            try:
                a = b.find('a')['href']

            except:
                continue 
            else:
                links.append(a)
                
        return links



    
    @staticmethod
    def store_in_redis(data):
        today = datetime.today()
        redis_client = RedisConf.create_connection_to_redis_server(True)
        for row in data:
            values_dict = {
                'Issuer Company': row[0],
                'Open': row[1],
                'Close': row[2],
                'Lot Size': row[3],
                'Issue Price ': row[4],
                'Cost of 1 lot': row[5]
            }
            try:
                ipo_closing_date = datetime.strptime(row[3], '%b %d, %Y')
            except Exception as e:
                print('❌ Invalid date format: ', e)
                return
            if ipo_closing_date > today:
                hash_name = REDIS_HASHES['ipo_details_v2']
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





        




        

       




        
       







