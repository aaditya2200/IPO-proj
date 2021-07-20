
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

def IPOscraper():
    URL = "https://www.chittorgarh.com/report/ipo-in-india-list-main-board-sme/82/"

    page = requests.get(URL)

    soup = BeautifulSoup(page.text , 'html.parser')

    htmltable = soup.find('table', { 'class' : 'table table-condensed table-bordered table-striped table-nonfluid table-hover' })



    def tableDataText(table):    
    
        def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
            return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
        rows = []
        trs = table.find_all('tr')
        headerow = rowgetDataText(trs[0], 'th')
        if headerow: # if there is a header row include first
            rows.append(headerow)
            trs = trs[1:]
        for tr in trs: # for every table row
            rows.append(rowgetDataText(tr, 'td') ) # data row       
        return rows


    list_table = tableDataText(htmltable)

    print(list_table[:2])

    return list_table[:2]