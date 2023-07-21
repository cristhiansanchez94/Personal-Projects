import matplotlib.pyplot as plt 
import matplotlib.dates as mdates

def draw_candlestick(stock_df):
    
    #This script assumes that the 200 moving average is already calculated and the 10% window around it. 
    
    
    plt.figure()
    
    # "up" dataframe will store the stock_prices 
    # when the closing stock price is greater
    # than or equal to the opening stock prices
    up = stock_df[stock_df.close >= stock_df.open]
    
    # "down" dataframe will store the stock_df
    # when the closing stock price is
    # lesser than the opening stock prices
    down = stock_df[stock_df.close < stock_df.open]
    
    # When the stock prices have decreased, then it
    # will be represented by blue color candlestick
    col1 = 'red'
    
    # When the stock prices have increased, then it 
    # will be represented by green color candlestick
    col2 = 'green'
    
    col3 = 'blue'
    
    col4 = 'orange'
    
    # Setting width of candlestick elements
    width = .3
    width2 = .03
    
    plt.plot(stock_df.index, stock_df.avg_200, color=col3)
    plt.plot(stock_df.index, stock_df.avg_200_up, color=col4)
    plt.plot(stock_df.index, stock_df.avg_200_bottom, color=col4)
    
    # Plotting up prices of the stock
    plt.bar(up.index, up.close-up.open, width, bottom=up.open, color=col1)
    plt.bar(up.index, up.high-up.close, width2, bottom=up.close, color=col1)
    plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color=col1)
    
    # Plotting down prices of the stock
    plt.bar(down.index, down.close-down.open, width, bottom=down.open, color=col2)
    plt.bar(down.index, down.high-down.open, width2, bottom=down.open, color=col2)
    plt.bar(down.index, down.low-down.close, width2, bottom=down.close, color=col2)
    ax = plt.gca()
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    
    # rotating the x-axis tick labels at 30degree 
    # towards right
    
    # displaying candlestick chart of stock data 
    # of a week
    plt.show()