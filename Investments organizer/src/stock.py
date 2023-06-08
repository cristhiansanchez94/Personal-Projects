import pandas as pd 
import numpy as np 

class Stock(): 
    def __init__(self, ticker:str, stock_df: pd.DataFrame, split_params: dict = {}): 
        self.ticker = ticker
        self.quantity = 0
        self.movements_df = stock_df
        self.bought_amount = 0 
        self.bought_amount_value = 0 
        self.sold_amount = 0 
        self.sold_amount_value = 0 
        self.remaining_amount_value = 0
        self.average_price = 0
        self.fifo_average_price = 0
        self.fifo_average_price_normal = 0
        self.stock_remainder_fifo = 0
        self.result = {}
        self.total_movements = []
        self.purchased_amounts = []
        self.purchased_prices = []
        self.purchase_flags = []
        self.min_date = stock_df.enteredAt.min()
        self.max_date = stock_df.enteredAt.max()
        self.split_factor = 0 
        self.remaining_quantity = 0 
        if split_params: 
            self.split_factor = split_params.get('factor')
            self.split_date = split_params.get('date')
            
    def reset_quantities(self):
        self.quantity = 0
        self.average_price = 0
        self.fifo_average_price = 0
        self.fifo_average_price_normal = 0
        self.purchased_amounts = []
        self.purchased_prices = []
        self.purchase_flags = []
        self.bought_amount_value = 0 
        self.sold_amount_value = 0 
        
    def correct_stock_quantity_and_price(self): 
        if self.quantity*self.average_price <0.05: 
            profit = 0 if self.bought_amount_value == 0 else self.sold_amount_value - self.bought_amount_value
            pl = -1 if self.bought_amount_value ==0 else round(profit / self.bought_amount_value,4)
            self.total_movements.append({
                'ticker':self.ticker,
                'min_date': self.min_date,
                'max_date':self.max_date,
                'bought_amount':self.bought_amount_value,
                'sold_amount':self.sold_amount_value,
                'profit': profit,
                'PL': pl}
                )
            self.reset_quantities()
    
    def update_purchase_flags(self, quantity): 
        first_flag_index = self.purchase_flags.index(1)
        accumulated_quantity = 0 
        for index in range(first_flag_index, len(self.purchase_flags)): 
            if accumulated_quantity + self.purchased_amounts[index]<=quantity: 
                accumulated_quantity += self.purchased_amounts[index]
                self.purchase_flags[index] = 0
            else: 
                self.stock_remainder_fifo = accumulated_quantity+self.purchased_amounts[index] - quantity 
                break        
        
            
    def register_movement(self,movement_type, quantity, movement_value, movement_price): 
        if movement_type == 1: 
            self.bought_amount += quantity
            self.bought_amount_value += movement_value
            self.purchased_amounts.append(quantity)
            self.purchased_prices.append(movement_price)
            self.purchase_flags.append(1)
        else: 
            self.sold_amount += quantity
            self.sold_amount_value += movement_value   
            if self.purchase_flags:  
                self.update_purchase_flags(quantity)
        
    def calculate_average_price(self, movement_type, quantity, price, methodology='Normal'): 
        if methodology=='Normal':
            if movement_type == 1:
                average_price = self.average_price 
                stock_quantity = self.quantity
                self.average_price = (average_price*stock_quantity + movement_type*quantity*price)/(stock_quantity + movement_type*quantity)
        else: 
            #Implement fifo methodology
            if self.purchase_flags:
                purchased_amounts = np.array(self.purchased_amounts)
                flags = np.array(self.purchase_flags)
                purchased_prices = np.array(self.purchased_prices)
                if methodology=='FIFO_normal':
                    if 1 in self.purchase_flags:
                        first_flag_index = self.purchase_flags.index(1)
                        current_active_quantity = self.purchased_amounts[first_flag_index]                        
                        quantity_correction = self.stock_remainder_fifo - current_active_quantity if self.stock_remainder_fifo!=0 else 0
                        price_for_correction = self.purchased_prices[first_flag_index]
                        amount_correction = quantity_correction * price_for_correction   
                    else: 
                        amount_correction = 0          
                        quantity_correction = 0      
                    self.fifo_average_price_normal = (np.dot(purchased_amounts*flags, purchased_prices)+amount_correction)/(np.sum(purchased_amounts*flags)+quantity_correction)
                else:
                    self.fifo_average_price = np.dot(purchased_amounts*flags, purchased_prices)/np.sum(purchased_amounts*flags)
                
                
    
    def update_quantity(self, movement_type, quantity): 
        self.quantity += movement_type*quantity
    
    def process_movements(self): 
        data = self.movements_df 
        data = data.query('status=="filled"').loc[:, ['enteredAt','side','symbol','filledQuantity','amount','price','feesUSD']]
        data = data.assign(movement_type = data.side.apply(lambda x: 1 if x=='BUY' else -1))
        data.sort_values(by='enteredAt',inplace=True)
        data.reset_index(drop=True, inplace=True)
        if self.split_factor >0: 
            corrected_df = data[data.enteredAt<self.split_date]
            normal_df = data[data.enteredAt>=self.split_date]
            split_factor = self.split_factor 
            corrected_df = corrected_df.assign(filledQuantity = corrected_df.filledQuantity*split_factor)
            corrected_df = corrected_df.assign(price = corrected_df.price/split_factor)
            data = pd.concat([corrected_df, normal_df],axis=0)
        self.movements_df = data
        
        if self.ticker=='BAC': 
            print('alto ahí')
        
        for idx in range(len(data)): 
            movement_data = data.loc[idx, :]            
            movement_type = movement_data['movement_type']
            movement_value = movement_data['amount']
            movement_price = movement_data['price']
            movement_quantity = movement_data['filledQuantity']
            movement_date = movement_data['enteredAt']
            if self.quantity==0: 
                self.min_date = movement_date 
            self.max_date = movement_date
            self.register_movement(movement_type, movement_quantity, movement_value, movement_price)
            self.calculate_average_price(movement_type, movement_quantity, movement_price)
            self.calculate_average_price(movement_type, movement_quantity, movement_price, methodology = 'FIFO')
            self.calculate_average_price(movement_type, movement_quantity, movement_price, methodology = 'FIFO_normal')
            self.update_quantity(movement_type, movement_quantity)
            self.correct_stock_quantity_and_price()
        
        current_value = round(self.average_price * self.quantity,2)
        if self.bought_amount_value<=self.sold_amount_value: 
            current_value = -1 
            self.remaining_quantity = self.remaining_quantity + self.quantity 
            self.quantity = 0 
            self.average_price = 0 
        self.remaining_amount_value = max(self.bought_amount_value-self.sold_amount_value, 0)
        self.result = {
                        'ticker': self.ticker,
                        'min_date': self.min_date,
                       'max_date': self.max_date,                       
                       'bought_amount': self.bought_amount_value, 
                       'sold_amount': self.sold_amount_value,  
                       'remaining_amount': self.remaining_amount_value,
                        'available_quantity': self.quantity, 
                       'remaining_quantity': self.remaining_quantity,
                       'fifo_average_price': round(self.fifo_average_price,2),
                       'fifo_average_price_normal': round(self.fifo_average_price_normal,2),
                       'average_price': round(self.average_price,2),
                       'total_fees': data['feesUSD'].sum(), 
                       'current_value': current_value                       
                       }
        
    
        
    
    