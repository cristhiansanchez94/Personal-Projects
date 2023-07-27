from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def scrape_assets_info(type='stocks'):
    '''Function used to scrape the basic information of an asset. 
        Inputs: 
        -type(str): The type of information to be scrapped. Should be either stocks or etf
        Outputs: 
        - assets_db(dict): A dictionary with the basic information of the assets. Primary key: Asset ticker
        - sectors_db(dict): A dicitonary with a grouping of the assets per sector/asset class. Primary key: sector/asset class
    '''
    driver = webdriver.Chrome()
    driver.get(f'https://stockanalysis.com/{type}/')
    source_codes = []
    element = driver.find_element(By.CSS_SELECTOR, "button[class='controls-btn xs:pl-1 xs:pr-1.5 bp:text-sm sm:pl-3 sm:pr-1']")

    while element.is_enabled():
        html = driver.page_source.encode('utf-8')
        source_codes.append(html)
        driver.execute_script("arguments[0].click();", element)
    html = driver.page_source.encode('utf-8')
    source_codes.append(html)
    driver.quit()
    soups = [BeautifulSoup(html,'html.parser') for html in source_codes]
    assets_db = {}
    sectors_db = {}
    for soup in soups: 
        table_items = soup.find_all('td')
        stock_amounts = len(table_items)/4
        for asset_index in range(int(stock_amounts)):
            asset_ticker = table_items[asset_index*4].text
            company_name = table_items[asset_index*4+1].text
            company_sector = table_items[asset_index*4+2].text
            if company_sector not in sectors_db: 
                sectors_db[company_sector] = [asset_ticker]
            else:
                sectors_db[company_sector].append(asset_ticker)
            if type=='stocks':
                assets_db[asset_ticker]={'company_name':company_name,'company_sector':company_sector}
            else: 
                assets_db[asset_ticker]={'asset_name':company_name,'asset_class':company_sector}
    return assets_db, sectors_db 

    