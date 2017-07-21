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

        self.max_price_list = {"STOCKS":[]}
        self.min_price_list = {"STOCKS":[]}

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
    order_history_index = order_history_index + 1
    json = '{"type": "add", "order_id": ' + str(
        history_trade_order_index) + ',"symbol": "' + symbol + '", "dir": "' + trade_direction + '", "price": ' + str(
        price) + ', "size" : ' + str(amount) + '}' # TODO: make sure json has correct format

    print(json, file=sys.stderr)
    print(json, file=exchange)

    my_portfolio.order_history[index] = Order(symbol, price, amount, trade_direction, my_portfolio)

def cancel_order(): # TODO: haven't implemented yet

# high level trading, buy & sell the max amount of stocks
def trigger_trade(symbol, exchange, fair_price, my_portfolio):
    buy = my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "BUY")
    sell = -1 * my_portfolio.holdings[symbol] + my_portfolio.pending_order_sum(symbol, "SELL")
    symbol_limit = my_portfolio.symbol_sum_limit[symbol]

    buy_amount = symbolLimit - buy
    sell_amount = symbolLimit - sell

    if buy < symbol_limit and buy_amount > 0:
        place_order(symbol, "BUY", fair_price - my_portfolio.spread, buy_amount, my_portfolio, exchange)
    if sell < symbol_limit and sell_amount > 0:
        place_order(symbol, "SELL", fair_price + my_portfolio.spread, sell_amount, my_portfolio, exchange)

def trade_bond(exchange, my_portfolio):
    fair_price = 1000
    place_order("BOND", "BUY", fair_price - 1, 100, my_portfolio, exchange)
    place_order("BOND", "SELL", fair_price + 1, 100, my_portfolio, exchange)

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

def main():
    # permission to trade each kind of stocks
    trade_bond = True
    trade_regular = True
    trade_complex_fund = True
    trade_simple_fund = True

    exchange = connect()
    json = '{"type":"hello","team":"?????"}' # TODO: fill in team name
    print(json, file=exchange)

    # parseMarketMessage???

    while True:
        market_info_raw = exchange.readline().strip()

        # error, print for debugging
        if market_info_raw is not None:
            if json.loads(market_info_raw)['type'] != 'ack' and json.loads(market_info_raw)['type'] != 'book' \
                    and json.loads(market_info_raw)['type'] != 'trade':
                print("@@@Log: %s" % str(market_info_raw), file=sys.stderr)

        if trade_bond:
            trigger_trade("BOND", exchange, 1000, my_portfolio)
        if trade_regular:

        if trade_complex_fund:

        if trade_simple_fund:
