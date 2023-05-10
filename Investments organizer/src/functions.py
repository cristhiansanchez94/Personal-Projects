import os

import pandas as pd 

import data_processing as dp 
from stock import Stock
 

SPLIT_DICT = {
    'GOOGL':{'factor':20,'date':'2022-07-18'}, 
    'GOOG':{'factor':20,'date':'2022-07-18'},
    'AMZN':{'factor':20, 'date': '2022-06-06'}, 
    'TSLA':{'factor':3, 'date':'2022-08-25'}, 
    'GE'  :{'factor':1281/1000, 'date':'2023-01-04'}
}

def generate_reports(split_already = True):
    data = dp.load_data()
    data.symbol = data.symbol.replace({'FB':'META'})
    symbol_group = data.groupby('symbol')
    stock_report = []
    pl_report = []
    split_dict = SPLIT_DICT if not split_already else {}
    for symbol in symbol_group:
        ticker = symbol[0]
        symbol_df = symbol[1]
        stock = Stock(ticker, symbol_df, split_params = split_dict)
        stock.process_movements()
        stock_data = stock.result
        stock_report.append(stock_data)
        if stock.total_movements: 
            pl_report.extend(stock.total_movements)
    stock_report = pd.DataFrame(stock_report)
    stock_report = stock_report.assign(portfolio_percentage=stock_report.remaining_amount/stock_report.remaining_amount.sum())
    pl_report = pd.DataFrame(pl_report)    
    return stock_report, pl_report

def save_report(stock_report, pl_report, path): 
    final_report = {}
    final_report['posiciones abiertas'] = dp.format_df(stock_report[(stock_report.available_quantity>0) | (stock_report.remaining_quantity>0)])
    final_report['performance'] = dp.format_df(pl_report)
    
    with pd.ExcelWriter(os.path.join(path,'reporte_acciones.xlsx')) as writer: 
        for column in ['posiciones abiertas','performance']: 
            final_report[column].to_excel(writer,sheet_name=column,index=False)
        writer.save()
