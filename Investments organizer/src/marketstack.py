import requests 
import json 
import os 


MS_API_KEY = os.environ.get('ms_api_key')
BASE_URL = "http://api.marketstack.com/v1/"

def get_stock_price(stock_symbols):
    '''Function used to fetch the current price of a stock ticker'''
    params={
        'access_key': MS_API_KEY
    }
    end_point = ''.join([BASE_URL,"tickers/",stock_symbols,"/intraday/latest"])
    api_result = requests.get(end_point, params)
    json_result = json.loads(api_result.text)
    return {
        "last_price": json_result['last']
    }