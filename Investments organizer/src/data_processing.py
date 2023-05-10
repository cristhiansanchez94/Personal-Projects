import pandas as pd 
from datahandler import DataHandler

COMPATIBILITY_DICT = {
    'Fecha':'enteredAt',
    'Tipo':'side',
    'Ticker':'symbol',
    'Shares':'filledQuantity',
    'Monto':'amount',
    'Price':'price'    
}

REPLACE_DICT = {
    'min_date': 'primer movimiento', 
    'max_date': 'ultimo movimiento',
    'bought_amount':'cantidad comprada (USD)', 
    'sold_amount':'cantidad vendida (USD)', 
    'available_quantity': 'acciones disponibles',
    'remaining_quantity': 'acciones remanentes',
    'remaining_amount': 'cantidad restante (USD)',
    'fifo_average_price': 'precio promedio (FIFO)', 
    'average_price': 'precio promedio',
    'total_fees': 'total fees',
    'current_value': 'valor actual', 
    'profit': 'ganancia', 
    'portfolio_percentage': 'porcentaje del portafolio'
}
def format_df(df): 
    return df.rename(columns= REPLACE_DICT)

def load_data(path=''): 
    data =  DataHandler().fetch_data().rename(columns=COMPATIBILITY_DICT) if path=='' else pd.read_csv(path)
    if 'feesUSD' not in data.columns: 
        data['feesUSD'] = 0 
    if 'status' not in data.columns:
        data['status'] = 'filled'
    if not 'BUY' in data.side.unique():
        data.side = data.side.map({'Compra':'BUY','Venta':'SELL'})
    return data