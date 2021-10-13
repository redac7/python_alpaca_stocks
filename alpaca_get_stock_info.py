import requests, json
from config import *
import alpaca_trade_api as tradeapi
import ipdb
from datetime import datetime, timedelta, date
import time

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
POSITION_URL = "{}/v2/positions".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY':SECRET_KEY}

# Gets the account information for ACCOUNT_URL
#
# returns: a list of the stocks in the account
def get_account():
    r = requests.get(ACCOUNT_URL, headers = HEADERS )

    return json.loads(r.content)

# This method creates an order and executes it in Alpace
# symbol:           The stock symbol you want to buy
# qty:              The number of stocks to buy
# side:             The option to buy or sell the stock
# type:             The option to buy at market or buy at a certain price
# time_in_force:    The option to buy at gtc "good till close"
#
# returns:          The response of the request post to buy stocks
def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force":time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)

# This method gets the position of stock in the portfolio
# stock_symbol: The stock symbol to check the position on
#
# return: the integer quantiy of stocks owned
def get_position(stock_symbol):
    #r = requests.post(POSITION_URL,headers=HEADERS)
    #return json.loads(r.content)
    api = tradeapi.REST()
    stock_position = 0
    try:
        # Get our position in stock.
        stock_position = api.get_position(stock_symbol)
    except:
        print("No position in {}".format(stock_symbol))
        return stock_position
    return stock_position.qty

# This method will get all the positions for the account
#
# returns:  A list of the the stocks and positions
def get_all_positions():
    # Get a list of all of our positions.
    api = tradeapi.REST()
    portfolio = api.list_positions()
    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))
    return portfolio

# This method will get the stock price for a stock that is passed in
# stock_symbol: The symbol or ticker of the stock to get the price of.
#
# returns:  The current price of the stock
def get_stock_price_alpaca(stock_symbol):
    api = tradeapi.REST()
    barset = api.get_barset(stock_symbol, 'day', limit=1)
    stock_barset=barset[stock_symbol]
    return stock_barset[0].c

# This method will get the stock volume for a stock that is passed in
# stock_symbol: The symbol or ticker of the stock to get the volume of.
#
# returns:  The current volume of the stock
def get_stock_volume_alpaca(stock_symbol):
    api = tradeapi.REST()
    barset = api.get_barset(stock_symbol, 'day', limit=1)
    stock_barset=barset[stock_symbol]
    return stock_barset[0].v

# This method will get the stock closing price for a stock that is passed in
#   on an older date that is passed in.
# stock_symbol: The symbol or ticker of the stock to get the price of
# old_date:     The date to get the closing price
#
# returns:  The price of the stock on the data that was passed in
def get_price_on_older_date(stock_symbol,old_date):
    #get todays date and calculate how many days ago old date was
    old_date_obj = datetime.strptime(old_date, '%m/%d/%y')
    days_back = (datetime.today() - old_date_obj).days
    api = tradeapi.REST()
    barset = api.get_barset(stock_symbol, 'day', limit=days_back)
    stock_barset=barset[stock_symbol]
    return stock_barset[0].c

# This method will get the stock closing volume for a stock that is passed in
#   on an older date that is passed in.
# stock_symbol: The symbol or ticker of the stock to get the volume of
# old_date:     The date to get the closing price
#
# returns:  The volume of the stock on the data that was passed in
def get_volume_on_older_date(stock_symbol,old_date):
    #get todays date and calculate how many days ago old date was
    old_date_obj = datetime.strptime(old_date, '%m/%d/%y')
    days_back = (datetime.today() - old_date_obj).days
    api = tradeapi.REST()
    barset = api.get_barset(stock_symbol, 'day', limit=days_back)
    stock_barset=barset[stock_symbol]
    return stock_barset[0].v


# Get the curent price of CSCO
print(f"The current price of CSCO is {get_stock_price_alpaca('CSCO')}")

# Get the curent volume of CSCO
print(f"The current volume of CSCO is {get_stock_volume_alpaca('NTAP')}")

# Get the price of CSCO on April 16th, 2021
print(f"The closing price of NTAP on April 16th, 2021 was {get_price_on_older_date('CSCO', '04/16/21')}")

# Get the volume of CSCO on April 16th, 2021
print(f"The volume on April 16th, 2021 was {get_volume_on_older_date('NTAP', '04/16/21')}")

# Get my position in my portfolio of CSCO
output = get_position('CSCO')
print(f"My current position for CSCO is {output}")

# Get all the stock positions in my portfolio
response = get_all_positions()
print(f"My current positions in my portfolio is {output}")

# Buy 100 shares of CSCO
stock = "csco"
response = create_order(stock.upper(), 100, "sell", "market", "gtc")
print(f"The output from the buy order was: {response}")
