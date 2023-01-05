import tkinter as tkt
from functions import generate_reports, save_report
import os 

class WrappingLabel(tkt.Label):
    '''a type of Label that automatically adjusts the wrap to the size'''
    def __init__(self, master=None, **kwargs):
        tkt.Label.__init__(self, master, **kwargs)
        self.bind('<Configure>', lambda e: self.config(wraplength=self.winfo_width()))

stock_report, pl_report = generate_reports()
stock_report = stock_report[(stock_report.available_quantity>0) | (stock_report.remaining_quantity>0)]
PATH = path = os.path.join(os.path.dirname(__file__))

def update_vars(*args):
    ticker = case_select_var.get()
    stock_info = stock_report[stock_report.ticker==ticker].to_dict(orient='list')
    stock_info = {key:stock_info.get(key)[0] for key in stock_info}
    print(stock_info)

#Window Geometry

window = tkt.Tk()
window.title('Stock controller')
window.geometry("600x525")
window.resizable(0,0)

#Labels Placement 
total_investment_title = tkt.Label(window, text = 'Total invested amount(account): ', fg='black', font='Verdana 15')
total_investment_title.place(x=0, y=20)
total_investment = tkt.Label(window, text = str(stock_report.bought_amount.sum()), fg='black', font='Verdana 18 bold')
total_investment.place(x=400, y=20)
share_label = tkt.Label(window, text='Share:', fg='black', font='Verdana 18')
share_label.place(x=0,y=50)
avg_price_title = tkt.Label(window, text='Avg. price:', fg='black', font='Verdana 18')
avg_price_title.place(x=0,y=80)
fifo_avg_price = tkt.Label(window, text='Avg. price (FIFO):', fg='black', font='Verdana 18')
fifo_avg_price.place(x=0,y=110)
first_movement_title = tkt.Label(window, text='First movement:', fg='black', font='Verdana 18')
first_movement_title.place(x=0,y=140)
last_movement_title = tkt.Label(window, text='Last movement:', fg='black', font='Verdana 18')
last_movement_title.place(x=0,y=170)
available_stocks_title = tkt.Label(window, text='Available stocks:', fg='black', font='Verdana 18')
available_stocks_title.place(x=0,y=200)
total_invested_amount_title = tkt.Label(window, text='Total invested amount (stock):', fg='black', font='Verdana 18')
total_invested_amount_title.place(x=0,y=230)
total_sold_amount_title= tkt.Label(window, text='Total sold amount:', fg='black', font='Verdana 18')
total_sold_amount_title.place(x=0,y=260)
portfolio_percentage_title= tkt.Label(window, text='Portfolio percentage:', fg='black', font='Verdana 18')
portfolio_percentage_title.place(x=0,y=290)

avg_price_calculator_title = tkt.Label(window, text='Avg. price calculator', fg='black', font='Verdana 20 bold')
avg_price_calculator_title.place(x=150,y=320)

desired_avg_price_title = WrappingLabel(window, text='Desired avg. price', fg='black', font='Verdana 18', width=10)
desired_avg_price_title.place(x=0, y=360)
required_amount_title = WrappingLabel(window, text='Required amount', fg='black', font='Verdana 18', width=10)
required_amount_title.place(x=0, y=410)

amount_to_invest_title = WrappingLabel(window, text='Amount to invest', fg='black', font='Verdana 18', width=10)
amount_to_invest_title.place(x=300, y=360)
nev_avg_price_title = WrappingLabel(window, text='New avg. price', fg='black', font='Verdana 18', width=10)
nev_avg_price_title.place(x=300, y=410)

#Button frame 
generate_report_button = tkt.Button(window, text='Save general report', width =50, command = lambda:save_report(stock_report, pl_report, PATH), state='normal')
generate_report_button.pack(side='bottom',pady=30)
 
 
 #Stock selector
cases = list(stock_report.ticker.unique())
case_select_var = tkt.StringVar(window)
case_select_var.set(cases[0])
 
options = tkt.OptionMenu(window, case_select_var, *cases, command = update_vars) 
options.config(width=15, font=('Verdana', 12))
options.place(x=350, y=50)
 



window.mainloop()
