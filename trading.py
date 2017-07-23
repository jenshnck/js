#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time

# portfolio
class Stock_Portfolio():
    def __init__(self, exchange):
        self.exchange = exchange

        self.order_history = {}
        self.order_history_index = 0

        self.holdings = {"BOND": 0, "STOCKS B": 0} #TODO: change with real stocks names
        self.symbol_sum_limit = {"BOND": 100, "STOCKS B": 100} #TODO: change with real stocks names
        self.spread = {"BOND": 1, "STOCKS B": 5} #TODO: change with real stocks names

        # penny-pinching
        self.stock_regular = ["A", "B", "C"];
        self.stock_simple_fund = ["A", "B", "C"];
        self.stock_complex_fund = ["A", "B", "C"];
        self.stock_bond = ["A", "B", "C"]

        self.max_price = {"A":0, "B":0}
        self.min_price = {"A":0, "B":0}

        self.indicator_prices = {}
        self.simple_fund_prices = {}

    # return the total amount of pending order of a stock
    def pending_order_sum(self, symbol, trade_direction):
        result = 0
        for history_index in self.order_history:
            order = self.order_history[history_index]
            if order.symbol == symbol and order.trade_direction == trade_direction:
                result = result + order.amount
        return result
# order
class Order():
    def __init__(self, symbol, price, amount, trade_direction, my_portfolio): #is_not_allow_fill?
        self.symbol = symbol
        self.price = price
        self.amount = amount
        self.trade_direction = trade_direction

def place_order(symbol, trade_direction, amount, my_portfolio, exchange):
    index = my_portfolio.order_history_index
    my_portfolio.order_history_index = index + 1
    json = '{"type": "add", "order_id": ' + str(
        index) + ',"symbol": "' + symbol + '", "dir": "' + trade_direction + '", "price": ' + str(
        price) + ', "size" : ' + str(amount) + '}' # TODO: make sure json has correct format

    print(json, file=sys.stderr)
    print(json, file=exchange)

    my_portfolio.order_history[index] = Order(symbol, price, amount, trade_direction, my_portfolio)

def cancel_order(): # TODO: haven't implemented yet

# high level trading, buy & sell the max amount of stocks
def penny_trade(symbol, exchange, my_portfolio):
    min_price = my_portfolio.min_price[symbol]
    max_price = my_portfolio.max_price[symbol]

    buy = my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "BUY")
    sell = -1 * my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "SELL")
    symbol_limit = my_portfolio.symbol_sum_limit[symbol]

    buy_amount = symbol_limit - buy
    sell_amount = symbol_limit - sell

    if buy < symbol_limit and buy_amount > 0:
        place_order(symbol, "BUY", max_price + my_portfolio.spread, buy_amount, my_portfolio, exchange) # TODO: potentially lose a lot of money against other ppl with the same strategy
    if sell < symbol_limit and sell_amount > 0:
        place_order(symbol, "SELL", min_price - my_portfolio.spread, sell_amount, my_portfolio, exchange) # TODO: potentially lose a lot of money against other ppl with the same strategy

def bond_trade(symbol, exchange, fair_price, my_portfolio):
    buy = my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "BUY")
    sell = -1 * my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "SELL")
    symbol_limit = my_portfolio.symbol_sum_limit[symbol]

    buy_amount = symbolLimit - buy
    sell_amount = symbolLimit - sell

    if buy < symbol_limit and buy_amount > 0:
        place_order(symbol, "BUY", fair_price - my_portfolio.spread, buy_amount, my_portfolio, exchange) # TODO: potentially lose a lot of money against other ppl with the same strategy
    if sell < symbol_limit and sell_amount > 0:
        place_order(symbol, "SELL", fair_price + my_portfolio.spread, sell_amount, my_portfolio, exchange) # TODO: potentially lose a lot of money against other ppl with the same strategy



def one_way(symbol, trade_direction, exchange, my_portfolio):

    buy = my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "BUY")
    sell = -1 * my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "SELL")
    symbol_limit = my_portfolio.symbol_sum_limit[symbol]

    buy_amount = symbolLimit - buy
    sell_amount = symbolLimit - sell

    if trade_direction == "BUY":
        max_price = my_portfolio.max_price[symbol]
        if buy < symbol_limit and buy_amount > 0:
            place_order(symbol, "BUY", max_price + my_portfolio.spread, buy_amount, my_portfolio, exchange)

    else:
        min_price = my_portfolio.min_price[symbol]
        if sell < symbol_limit and sell_amount > 0:
            place_order(symbol, "SELL", min_price - my_portfolio.spread, sell_amount, my_portfolio, exchange)


def parse_market_message(market_message, my_portfolio):
    data = json.loads(market_message)

    if data['type'] == 'out': # TODO: check if market message is in this format

    elif data['type'] == 'book':

    elif data['type'] == 'fill':

    elif data['type'] == 'trade': # and dat['symbol'] not in ["VALE", "BOND"]???

    elif data['type'] == 'hello':


# connect to server
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TODO: change parameters on the day
    # parameters: teamname, port number
    s.connect(("team name", 000))
    # parameters: mode, bufsize
    return s.makefile('w+', 1)

def update_max_min(price_info, my_portfolio):

    if price_info['symbol'] in my_portfolio.max_price:
        symbol = price_info['symbol']
        my_portfolio.max_price[symbol] = price_info['buy'][0] # TODO: analyze book object structure key is buy and value is an array
    if price_info['symbol'] in my_portfolio.min_price:
        symbol = price_info['symbol']
        my_portfolio.min_price[symbol] = price_info['sell'][0] # TODO: analyze book object structure key is sell and value is an array

def fill(fill_info, my_portfolio):

    order = my_portfolio.order_history[fill_info['order_id']]
    # Trade_Ticket.fill(current_market['size'], myTrade_Portfolio)

    fill_amount = fill_info['size'];

    order.amount -= fill_amount

    if order.trade_direction == "BUY":
        my_portfolio.holdings[order.symbol] += fillAmount
    else:
        my_portfolio.holdings[order.symbol] -= fillAmount

def simple_fund_trade(market_message, my_portfolio):
    convertion = True

    indicator_price = my_portfolio.max_price["NAME"] # TODO: edit indicator name for simple fund
    fund_price = my_portfolio.max_price["NAME"]       # TODO: get simple fund name

    indicator_price_fair_price = (my_portfolio.max_price["NAME"] + my_portfolio.min_price["NAME"])/2 # TODO: edit indicator name for simple fund
    fund_price_min = my_portfolio.min_price["NAME"]      # TODO: get simple fund name
    fund_price_max = my_portfolio.max_price["NAME"]

    if convertion :
        one_way("fund_name", "BUY", my_portfolio, exchange) #TODO: fund_name
        if my_portfolio.symbol_sum_limit["fund_name"] * fund_price + 2 < my_portfolio.symbol_sum_limit["indicator_name"] * indicator_price :       # TODO: verify conversion rate
            if my_portfolio.holdings["fund_name"] == my_portfolio.symbol_sum_limit["fund_name"]: # if holdings are sufficient
                convert("SELL", my_portfolio.symbol_sum_limit["fund_name"], my_portfolio, exchange)  #TODO: fund_name
                one_way("indicator_name", "SELL", my_portfolio, exchange) #TODO: indicator_name

        elif my_portfolio.symbol_sum_limit["indicator_name"] * indicator_price + 2 < my_portfolio.symbol_sum_limit["fund_name"] * fund_price:
            if my_portfolio.holdings["indicator_name"] == my_portfolio.symbol_sum_limit["indicator_name"]: # if holdings are sufficient
                convert("BUY", my_portfolio.symbol_sum_limit["indicator_name"], my_portfolio, exchange)  #TODO: indicator_name 1:1 conversion?
                one_way("fund_name", "SELL", my_portfolio, exchange) #TODO: indicator_name
    else :
        if fund_price_max > indicator_price_fair_price:
            one_way("fund_name", "SELL", my_portfolio, exchange)
        else if fund_price_min < indicator_price_fair_price:
            one_way("fund_name", "BUY", my_portfolio, exchange) #TODO: fund_name
            if my_portfolio.holdings["fund_name"] == my_portfolio.symbol_sum_limit["fund_name"]: # if holdings are sufficient
                convert("SELL", my_portfolio.symbol_sum_limit["fund_name"], my_portfolio, exchange)  #TODO: fund_name
                one_way("indicator_name", "SELL", my_portfolio, exchange) #TODO: indicator_name


def convert_simple(trade_direction, amount, my_portfolio, exchange):
    index = my_portfolio.order_history_index
    my_portfolio.order_history_index = index + 1

    json = '{"type": "convert", "order_id": %d' % index + ', "symbol": "SIMPLE_NAME", "dir": "' + trade_direction + '", "size": %s}' % str( #TODO: add  Simple name
        amount)

    print(json, file=exchange)
    # TODO: adapt balances accordingly
    my_portfolio.order_history[index] = Order("fund_name", -1, amount, trade_direction,
                                                                                   myTrade_Portfolio) # is_not_allow_fill=True

    if trade_direction == "BUY":
        sign = +1
    else:
        sign = -1

    #convert stocks to XLF
    my_portfolio.holdings["indicator_name"] -= sign * 0 * amount / 1 # TODO update indicator name and ratio
    my_portfolio.holdings["fund_name"] += sign * amount

def convertXLF(trade_direction, amount, myTrade_Portfolio, exchange):
    # increase the counter of the id

    index = my_portfolio.order_history_index
    myTrade_Portfolio.order_history_index += 1

    json_string = '{"type": "convert", "order_id": %d' % index + ', "symbol": "XLF", "dir": "' + trade_direction + '", "size": %s}' % str(
        amount)

    print(json_string, file=exchange)
    my_portfolio.order_history[index] = Order("XLF", -1, amount, trade_direction, myTrade_Portfolio)

    if trade_direction == "BUY":
        sign = +1
    else:
        sign = -1

    #convert stocks to XLF
    myTrade_Portfolio.positions_sym["BOND"] -= sign * 3 * amount / 10
    myTrade_Portfolio.positions_sym["GS"] -= sign * 2 * amount / 10
    myTrade_Portfolio.positions_sym["MS"] -= sign * 3 * amount / 10
    myTrade_Portfolio.positions_sym["WFC"] -= sign * 2 * amount / 10
    myTrade_Portfolio.positions_sym["XLF"] += sign * amount

def main():
    # permission to trade each kind of stocks
    trade_bond = True  # 1
    trade_regular = False  # penny-pinching 2 --> identify delay for simple fund trading
    trade_complex_fund = False  # decompostion 3
    trade_simple_fund = False  # tracing 3

    exchange = connect()
    json = '{"type":"hello","team":"?????"}' # TODO: fill in team name
    print(json, file=exchange)

    my_portfolio = Stock_Portfolio(exchange)

    while True:
        market_info_raw = exchange.readline().strip()

        market_info = json.loads(market_info_raw)

        # error, print for debugging  --> not ERROR! just used for personal recordkepping--> statistical analysis
        if market_info_raw is not None:
            if market_info['type'] != 'ack' and market_info['type'] != 'book' \
                    and market_info['type'] != 'trade':
                print("@@@Log: %s" % str(market_info_raw), file=sys.stderr)

        if trade_bond:
            bond_trade("BOND", exchange, 1000, my_portfolio) #TODO: fair price

        #update
        if(market_info['type'] == 'book'):
            update_max_min(market_info, my_portfolio)

        if(market_info['type'] == 'fill'):
            fill(market_info, my_portfolio)

        if trade_regular:
            for stock in my_portfolio.stock_regular: # for regular stocks trigger  trade --> penny pitch max and min
                if(my_portfolio.max_price[stock] != 0 and my_portfolio.min_price[stock] != 0):
                    penny_trade(stock, exchange, my_portfolio)

        if trade_simple_fund:
            for stock in my_portfolio.stock_simple_fund:
                if(my_portfolio.max_price[stock] != 0 and my_portfolio.min_price[stock] != 0):
                    simple_fund_trade()

        if trade_complex_fund:
            component_price = 0  # calculate the price of the fund according to respective composition
            # get highest price for all components --> max_price_list
            if component_price > current_fund_price:
                # buy fund --> convert to component and sell individual components
            else:
                # buy individual components --> convert to fund and sell all

        if trade_simple_fund:
            # get increses or decreases of indicator 0/5/10/20/50 ticks?
            # buy or sell fund accordingly
            # set timer index to appropriate number of ticks
            # if market_info_raw is not None: --> increase tick counter +1 one until tracing distance is reached --> buy/sell all inversly
