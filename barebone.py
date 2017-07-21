#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time

class Stock_Portfolio():
    def __init__(self, exchange):
        self.exchange = exchange

        self.order_history = {}
        self.order_history_index = 0

        self.holdings = {"BOND": 0, "STOCKS B": 0} #TODO: change with real stocks names
        self.symbol_sum_limit = {"BOND": 100, "STOCKS B": 100} #TODO: change with real stocks names
        self.spread = {"BOND": 1, "STOCKS B": 5} #TODO: change with real stocks names
        
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

    exchange = connect()
    json = '{"type":"hello","team":"?????"}' # TODO: fill in team name
    print(json, file=exchange)

    my_portfolio = Stock_Portfolio(exchange)

    while True:
        market_info_raw = exchange.readline().strip()

        # error, print for debugging  --> not ERROR! just used for personal recordkepping--> statistical analysis
        if market_info_raw is not None:
            if json.loads(market_info_raw)['type'] != 'ack' and json.loads(market_info_raw)['type'] != 'book' \
                    and json.loads(market_info_raw)['type'] != 'trade':
                print("@@@Log: %s" % str(market_info_raw), file=sys.stderr)

        if trade_bond:
            bond_trade("BOND", exchange, 1000, my_portfolio)
