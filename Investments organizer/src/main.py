import tkinter as tkt
from datetime import datetime 
import os 

from wrappinglabel import WrappingLabel
from functions import generate_reports, save_report


stock_report, pl_report = generate_reports()
stock_report = stock_report[(stock_report.available_quantity>0) | (stock_report.remaining_quantity>0)]
PATH = path = os.path.join(os.path.dirname(__file__))
TICKERS = list(stock_report.ticker.unique())
LABELS_X = 440

def get_info_for_ticker(ticker): 
    stock_info = stock_report[stock_report.ticker==ticker].to_dict(orient='list')
    stock_info = {key:stock_info.get(key)[0] for key in stock_info}
    return stock_info

def set_values_in_vars(ticker_info): 
    avg_price_var.set(ticker_info.get('average_price'))
    fifo_avg_price_var.set(ticker_info.get('fifo_average_price'))
    first_movement_var.set(datetime.strftime(ticker_info.get('min_date'),'%Y-%m-%d'))
    last_movement_var.set(datetime.strftime(ticker_info.get('max_date'),'%Y-%m-%d'))
    available_stocks_var.set(round(ticker_info.get('available_quantity'),2))
    remaining_stocks_var.set(round(ticker_info.get('remaining_quantity'),2))
    total_invested_amount_var.set(round(ticker_info.get('bought_amount'),2))
    total_sold_amount_var.set(round(ticker_info.get('sold_amount'),2))
    portfolio_percentage_var.set(str(round(ticker_info.get('portfolio_percentage')*100,2))+'%')
    required_amount_var.set('')
    new_avg_price_var.set('')
    desired_avg_price_var.set('')
    amount_to_invest_var.set('')

def update_vars(*args):
    ticker = case_select_var.get()
    stock_info = get_info_for_ticker(ticker)
    set_values_in_vars(stock_info)

#Window Geometry

window = tkt.Tk()
window.title('Stock controller')
window.geometry("600x580")
window.resizable(0,0)

#Variables 
avg_price_var = tkt.StringVar(window)
fifo_avg_price_var = tkt.StringVar(window)
first_movement_var = tkt.StringVar(window)
last_movement_var = tkt.StringVar(window)
available_stocks_var = tkt.StringVar(window)
remaining_stocks_var = tkt.StringVar(window)
total_invested_amount_var = tkt.StringVar(window)
total_sold_amount_var = tkt.StringVar(window)
portfolio_percentage_var = tkt.StringVar(window)
desired_avg_price_var = tkt.StringVar(window)
required_amount_var = tkt.StringVar(window)
amount_to_invest_var = tkt.StringVar(window)
new_avg_price_var = tkt.StringVar(window)

set_values_in_vars(get_info_for_ticker(TICKERS[0]))

#Labels Placement 
total_investment_title = tkt.Label(window, text = 'Total invested amount(account): ', fg='black', font='Verdana 15')
total_investment_title.place(x=0, y=20)
total_investment = tkt.Label(window, text = str(stock_report.bought_amount.sum()), fg='black', font='Verdana 18 bold')
total_investment.place(x=400, y=20)

share_label = tkt.Label(window, text='Share:', fg='black', font='Verdana 18')
share_label.place(x=0,y=50)

avg_price_title = tkt.Label(window, text='Avg. price:', fg='black', font='Verdana 18')
avg_price_title.place(x=0,y=80)
avg_price_label = tkt.Label(window, textvariable=avg_price_var, fg='black', font='Verdana 16')
avg_price_label.place(x=LABELS_X, y=80)

fifo_avg_price = tkt.Label(window, text='Avg. price (FIFO):', fg='black', font='Verdana 18')
fifo_avg_price.place(x=0,y=110)
fifo_avg_price_label = tkt.Label(window, textvariable=fifo_avg_price_var, fg='black', font='Verdana 16')
fifo_avg_price_label.place(x=LABELS_X, y=110)

first_movement_title = tkt.Label(window, text='First movement:', fg='black', font='Verdana 18')
first_movement_title.place(x=0,y=140)
first_movement_label = tkt.Label(window, textvariable=first_movement_var, fg='black', font='Verdana 16')
first_movement_label.place(x=LABELS_X, y=140)

last_movement_title = tkt.Label(window, text='Last movement:', fg='black', font='Verdana 18')
last_movement_title.place(x=0,y=170)
last_movement_label = tkt.Label(window, textvariable=last_movement_var, fg='black', font='Verdana 16')
last_movement_label.place(x=LABELS_X, y=170)

available_stocks_title = tkt.Label(window, text='Available stocks:', fg='black', font='Verdana 18')
available_stocks_title.place(x=0,y=200)
available_stocks_label = tkt.Label(window, textvariable=available_stocks_var, fg='black', font='Verdana 16')
available_stocks_label.place(x=LABELS_X, y=200)

remaining_stocks_title = tkt.Label(window, text='Remaining stocks:', fg='black', font='Verdana 18')
remaining_stocks_title.place(x=0,y=230)
remaining_stocks_label = tkt.Label(window, textvariable=remaining_stocks_var, fg='black', font='Verdana 16')
remaining_stocks_label.place(x=LABELS_X, y=230)

total_invested_amount_title = tkt.Label(window, text='Total invested amount (stock):', fg='black', font='Verdana 18')
total_invested_amount_title.place(x=0,y=260)
total_invested_amount_label = tkt.Label(window, textvariable=total_invested_amount_var, fg='black', font='Verdana 16')
total_invested_amount_label.place(x=LABELS_X, y=260)

total_sold_amount_title= tkt.Label(window, text='Total sold amount:', fg='black', font='Verdana 18')
total_sold_amount_title.place(x=0,y=290)
total_sold_amount_label = tkt.Label(window, textvariable=total_sold_amount_var, fg='black', font='Verdana 16')
total_sold_amount_label.place(x=LABELS_X, y=290)

portfolio_percentage_title= tkt.Label(window, text='Portfolio percentage:', fg='black', font='Verdana 18')
portfolio_percentage_title.place(x=0,y=320)
portfolio_percentage_label = tkt.Label(window, textvariable=portfolio_percentage_var, fg='black', font='Verdana 16')
portfolio_percentage_label.place(x=LABELS_X, y=320)



#Avg price calculator 

avg_price_calculator_title = tkt.Label(window, text='Avg. price calculator', fg='black', font='Verdana 20 bold')
avg_price_calculator_title.place(x=150,y=350)
current_price_title = WrappingLabel(window, text='Current price', fg='black', font='Verdana 18', width=10)
current_price_title.place(x=0, y=390)
desired_avg_price_title = WrappingLabel(window, text='Desired avg. price', fg='black', font='Verdana 18', width=10)
desired_avg_price_title.place(x=120, y=390)
required_amount_title = WrappingLabel(window, text='Required amount', fg='black', font='Verdana 18', width=10)
required_amount_title.place(x=240, y=390)

amount_to_invest_title = WrappingLabel(window, text='Amount to invest', fg='black', font='Verdana 18', width=10)
amount_to_invest_title.place(x=360, y=390)
nev_avg_price_title = WrappingLabel(window, text='New avg. price', fg='black', font='Verdana 18', width=10)
nev_avg_price_title.place(x=480, y=390)

#Button frame 
generate_report_button = tkt.Button(window, text='Save general report', width =50, command = lambda:save_report(stock_report, pl_report, PATH), state='normal')
generate_report_button.pack(side='bottom',pady=30)
 
 
 #Stock selector
case_select_var = tkt.StringVar(window)
case_select_var.set(TICKERS[0])
 
options = tkt.OptionMenu(window, case_select_var, *TICKERS, command = update_vars) 
options.config(width=15, font=('Verdana', 12))
options.place(x=390, y=50)
 



window.mainloop()
