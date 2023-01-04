import traceback 
import pandas as pd 
from stock import Stock
import os 

SPLIT_DICT = {
    'GOOGL':{'factor':20,'date':'2022-07-18'}, 
    'GOOG':{'factor':20,'date':'2022-07-18'},
    'AMZN':{'factor':20, 'date': '2022-06-06'}, 
    'TSLA':{'factor':3, 'date':'2022-08-25'}
}
REPLACE_DICT = {
    'min_date': 'primer movimiento', 
    'max_date': 'ultimo movimiento',
    'bought_amount':'cantidad comprada (USD)', 
    'sold_amount':'cantidad vendida (USD)', 
    'available_quantity': 'acciones disponibles',
    'remaining_quantity': 'acciones remanentes',
    'average_price': 'precio promedio',
    'total_fees': 'total fees',
    'current_value': 'valor actual', 
    'profit': 'ganancia', 
    'portfolio_percentage': 'porcentaje del portafolio'
}
def format_df(df): 
    return df.rename(columns= REPLACE_DICT)

def load_data(path): 
    return pd.read_csv(path) 

def main():
    path = os.path.join(os.path.dirname(__file__),'../history')
    file_name = 'orders.csv'    
    data = load_data(os.path.join(path,file_name))
    data.symbol = data.symbol.replace({'FB':'META'})
    symbol_group = data.groupby('symbol')
    stock_report = []
    pl_report = []
    final_report = {}
    for symbol in symbol_group:
        ticker = symbol[0]
        symbol_df = symbol[1]
        stock = Stock(ticker, symbol_df, split_params = SPLIT_DICT.get(ticker,{}))
        stock.process_movements()
        stock_data = stock.result
        stock_report.append(stock_data)
        if stock.total_movements: 
            pl_report.extend(stock.total_movements)
    stock_report = pd.DataFrame(stock_report)
    stock_report = stock_report.assign(portfolio_percentage=stock_report.bought_amount/stock_report.bought_amount.sum())
    pl_report = pd.DataFrame(pl_report)
    final_report['posiciones abiertas'] = format_df(stock_report[(stock_report.available_quantity>0) | (stock_report.remaining_quantity>0)])
    final_report['performance'] = format_df(pl_report)
    
    with pd.ExcelWriter(os.path.join(path,'reporte_passfolio.xlsx')) as writer: 
        for column in ['posiciones abiertas','performance']: 
            final_report[column].to_excel(writer,sheet_name=column,index=False)
        writer.save()

if __name__ == '__main__': 
    main()