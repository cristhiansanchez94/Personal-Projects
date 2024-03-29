from tkinter import StringVar, Tk, Label, Entry, Button, OptionMenu, Toplevel
from datetime import datetime 
from os.path import join, dirname

from wrappinglabel import WrappingLabel
from reports_handler import generate_reports, save_report
from marketstack import get_stock_price


stock_report, pl_report, movements_df= generate_reports()
stock_report = stock_report[(stock_report.available_quantity>0) | (stock_report.remaining_quantity>0)]
PATH = join(dirname(__file__))
TICKERS = list(stock_report.ticker.unique())
LABELS_X = 440

def get_info_for_ticker(ticker): 
    stock_info = stock_report[stock_report.ticker==ticker].to_dict(orient='list')
    stock_info = {key:stock_info.get(key)[0] for key in stock_info}
    try:
        last_price = get_stock_price(ticker)['last_price']
        stock_info['last_price'] = last_price 
        stock_info['current_value'] = (stock_info.get('available_quantity')+stock_info.get('remaining_quantity'))*last_price
    except: 
        stock_info['last_price'] = 'NA'
        stock_info['current_value'] = 'NA'
    return stock_info

def set_values_in_vars(ticker_info): 
    avg_price_var.set(ticker_info.get('average_price'))
    real_current_price_var.set(ticker_info.get('last_price'))
    current_value_var.set(round(ticker_info.get('current_value'),2))
    fifo_avg_price_var.set(str(ticker_info.get('fifo_average_price'))+"/"+str(ticker_info.get('fifo_average_price_normal')))
    first_movement_var.set(datetime.strftime(ticker_info.get('min_date'),'%Y-%m-%d'))
    last_movement_var.set(datetime.strftime(ticker_info.get('max_date'),'%Y-%m-%d'))
    available_stocks_var.set(round(ticker_info.get('available_quantity'),2))
    remaining_stocks_var.set(round(ticker_info.get('remaining_quantity'),2))
    total_invested_amount_var.set(round(ticker_info.get('bought_amount'),2))
    total_sold_amount_var.set(round(ticker_info.get('sold_amount'),2))
    portfolio_percentage_var.set(str(round(ticker_info.get('portfolio_percentage')*100,2))+'%')
    new_avg_price_var.set('')
    required_amount_var.set('')
    current_price_var.set('')
    desired_avg_price_var.set('')
    amount_to_invest_var.set('')
    
def update_vars(*args):
    ticker = case_select_var.get()
    stock_info = get_info_for_ticker(ticker)
    set_values_in_vars(stock_info)
    
def update_calculations_with_current_price(*args): 
    current_price = current_price_var.get()
    if current_price=='': 
        required_amount_var.set('')
        new_avg_price_var.set('')
    else: 
        desired_avg_price = desired_avg_price_var.get()
        amount_to_invest = amount_to_invest_var.get()
        if desired_avg_price!='': 
            calculate_required_amount(*args)
        if amount_to_invest!='':
            calculate_new_average_price(*args)
    
def calculate_required_amount(*args):
    current_price = current_price_var.get()
    desired_avg_price = desired_avg_price_var.get()
    if current_price!='' and desired_avg_price!='':        
        current_price = float(current_price)
        average_price = float(avg_price_var.get())
        stocks_quantity = float(available_stocks_var.get())
        desired_avg_price = float(desired_avg_price)
        required_amount_var.set(round(stocks_quantity*(desired_avg_price - average_price)/(1 - (desired_avg_price/current_price)),2))
    else: 
        required_amount_var.set('')
        
def create_saved_report_window():
    '''Function used to create a window with a message
    Inputs: 
     - message: The message to be posted 
     - error: Indicator if the message is an error o a simple message 
    ''' 
    global window 
    message_window = Toplevel(window)
    message_window.title('')
    message_window.geometry("350x100")
    message_window.resizable(0,0)
    message = 'Report saved succesfully'
    Label(message_window, text=message, fg='black', font='Verdana 12').place(x=40,y=20)
    Button(message_window, text='Ok', width=20, command=message_window.destroy).place(x=70,y=60)
 
        
def save_report_flow(stock_report,pl_report,path):
    save_report(stock_report,pl_report,path)
    create_saved_report_window()

def calculate_new_average_price(*args):
    current_price = current_price_var.get()
    amount_to_invest = amount_to_invest_var.get()
    if current_price!='' and amount_to_invest!='':
        current_price = float(current_price)
        average_price = float(avg_price_var.get())
        stocks_quantity = float(available_stocks_var.get())
        amount_to_invest = float(amount_to_invest)
        new_avg_price_var.set(round((average_price*stocks_quantity+amount_to_invest)/(stocks_quantity+amount_to_invest/current_price),2))
    else: 
        new_avg_price_var.set('')

#Window Geometry

window = Tk()
window.title('Stock controller')
window.geometry("600x600")
window.resizable(0,0)

#Variables 
avg_price_var = StringVar(window)
real_current_price_var = StringVar(window)
current_value_var = StringVar(window)
fifo_avg_price_var = StringVar(window)
first_movement_var = StringVar(window)
last_movement_var = StringVar(window)
available_stocks_var = StringVar(window)
remaining_stocks_var = StringVar(window)
total_invested_amount_var = StringVar(window)
total_sold_amount_var = StringVar(window)
portfolio_percentage_var = StringVar(window)
current_price_var = StringVar(window)
desired_avg_price_var = StringVar(window)
required_amount_var = StringVar(window)
amount_to_invest_var = StringVar(window)
new_avg_price_var = StringVar(window)

#set default value for variables
set_values_in_vars(get_info_for_ticker(TICKERS[0]))

#Labels Placement 
total_investment_title = Label(window, text = 'Total invested amount(account): ', fg='black', font='Verdana 15')
total_investment_title.place(x=0, y=20)
total_investment = Label(window, text = str(stock_report.remaining_amount.sum()), fg='black', font='Verdana 18 bold')
total_investment.place(x=LABELS_X, y=20)

share_label = Label(window, text='Share:', fg='black', font='Verdana 18')
share_label.place(x=0,y=50)

real_current_price_title = Label(window, text='Current price:', fg='black', font='Verdana 18')
real_current_price_title.place(x=0,y=80)
real_current_price_label = Label(window, textvariable=real_current_price_var, fg='black', font='Verdana 16')
real_current_price_label.place(x=LABELS_X, y=80)

current_value_title = Label(window, text='Current value:', fg='black', font='Verdana 18')
current_value_title.place(x=0,y=110)
current_value_label = Label(window, textvariable=current_value_var, fg='black', font='Verdana 16')
current_value_label.place(x=LABELS_X, y=110)

avg_price_title = Label(window, text='Avg. price:', fg='black', font='Verdana 18')
avg_price_title.place(x=0,y=140)
avg_price_label = Label(window, textvariable=avg_price_var, fg='black', font='Verdana 16')
avg_price_label.place(x=LABELS_X, y=140)

fifo_avg_price = Label(window, text='Avg. price (FIFO):', fg='black', font='Verdana 18')
fifo_avg_price.place(x=0,y=170)
fifo_avg_price_label = Label(window, textvariable=fifo_avg_price_var, fg='black', font='Verdana 16')
fifo_avg_price_label.place(x=LABELS_X, y=170)

first_movement_title = Label(window, text='First movement:', fg='black', font='Verdana 18')
first_movement_title.place(x=0,y=200)
first_movement_label = Label(window, textvariable=first_movement_var, fg='black', font='Verdana 16')
first_movement_label.place(x=LABELS_X, y=200)

last_movement_title = Label(window, text='Last movement:', fg='black', font='Verdana 18')
last_movement_title.place(x=0,y=230)
last_movement_label = Label(window, textvariable=last_movement_var, fg='black', font='Verdana 16')
last_movement_label.place(x=LABELS_X, y=230)

available_stocks_title = Label(window, text='Available stocks:', fg='black', font='Verdana 18')
available_stocks_title.place(x=0,y=260)
available_stocks_label = Label(window, textvariable=available_stocks_var, fg='black', font='Verdana 16')
available_stocks_label.place(x=LABELS_X, y=260)

remaining_stocks_title = Label(window, text='Remaining stocks:', fg='black', font='Verdana 18')
remaining_stocks_title.place(x=0,y=290)
remaining_stocks_label = Label(window, textvariable=remaining_stocks_var, fg='black', font='Verdana 16')
remaining_stocks_label.place(x=LABELS_X, y=290)

total_invested_amount_title = Label(window, text='Total invested amount (stock):', fg='black', font='Verdana 18')
total_invested_amount_title.place(x=0,y=320)
total_invested_amount_label = Label(window, textvariable=total_invested_amount_var, fg='black', font='Verdana 16')
total_invested_amount_label.place(x=LABELS_X, y=320)

total_sold_amount_title= Label(window, text='Total sold amount:', fg='black', font='Verdana 18')
total_sold_amount_title.place(x=0,y=350)
total_sold_amount_label = Label(window, textvariable=total_sold_amount_var, fg='black', font='Verdana 16')
total_sold_amount_label.place(x=LABELS_X, y=350)

portfolio_percentage_title= Label(window, text='Portfolio percentage:', fg='black', font='Verdana 18')
portfolio_percentage_title.place(x=0,y=380)
portfolio_percentage_label = Label(window, textvariable=portfolio_percentage_var, fg='black', font='Verdana 16')
portfolio_percentage_label.place(x=LABELS_X, y=380)



#Avg price calculator 

avg_price_calculator_title = Label(window, text='Avg. price calculator', fg='black', font='Verdana 20 bold')
avg_price_calculator_title.place(x=150,y=410)

current_price_title = WrappingLabel(window, text='Current price', fg='black', font='Verdana 18', width=10)
current_price_title.place(x=0, y=450)
current_price_entry = Entry(window, width=8, textvariable=current_price_var, justify='center', font=('verdana', 18))
current_price_entry.place(x=15, y=500)

desired_avg_price_title = WrappingLabel(window, text='Desired avg. price', fg='black', font='Verdana 18', width=10)
desired_avg_price_title.place(x=120, y=450)
desired_avg_entry = Entry(window, width=8, textvariable=desired_avg_price_var, justify='center', font=('verdana', 18))
desired_avg_entry.place(x=135, y=500)

required_amount_title = WrappingLabel(window, text='Required amount', fg='black', font='Verdana 18', width=10)
required_amount_title.place(x=240, y=450)
required_amount_label = Label(window, textvariable=required_amount_var, fg='black', font='Verdana 18', width=10)
required_amount_label.place(x=255, y=500)

amount_to_invest_title = WrappingLabel(window, text='Amount to invest', fg='black', font='Verdana 18', width=10)
amount_to_invest_title.place(x=360, y=450)
amount_to_invest_entry = Entry(window, width=8, textvariable=amount_to_invest_var, justify='center', font=('verdana', 18))
amount_to_invest_entry.place(x=375, y=500)

new_avg_price_title = WrappingLabel(window, text='New avg. price', fg='black', font='Verdana 18', width=10)
new_avg_price_title.place(x=480, y=450)
new_avg_price_label = Label(window, textvariable=new_avg_price_var, fg='black', font='Verdana 18', width=10)
new_avg_price_label.place(x=495, y=500)


amount_to_invest_var.trace("w",calculate_new_average_price)
desired_avg_price_var.trace("w",calculate_required_amount)
current_price_var.trace("w",update_calculations_with_current_price)

#Button frame 
generate_report_button = Button(window, text='Save general report', width =50, command = lambda:save_report_flow(stock_report, pl_report, PATH), state='normal')
generate_report_button.pack(side='bottom',pady=30)
 
 
 #Stock selector
case_select_var = StringVar(window)
case_select_var.set(TICKERS[0])
 
options = OptionMenu(window, case_select_var, *TICKERS, command = update_vars) 
options.config(width=15, font=('Verdana', 12))
options.place(x=390, y=50)
 



window.mainloop()
