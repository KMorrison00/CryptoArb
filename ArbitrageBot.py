from catalyst.utils.run_algo import run_algorithm
from catalyst.api import symbol, order
import pandas as pd



def is_profitable_after_fees(sell_price, buy_price, sell_market, buy_market):
    sell_fee = get_fee(sell_market,sell_price)
    buy_fee = get_fee(buy_market,buy_price)
    expected_profit = sell_price - buy_price - sell_fee - buy_fee

    if expected_profit > 0:
        print("Sell {} at {}, Buy {} at {}".format(sell_market.name, sell_price, buy_market.name, buy_price))
        print("Total fees: {}".format(buy_fee+sell_fee))
        print("Expected profit: {}".format(expected_profit))
        return True
    return False


def get_fee(market, price):
    return round(market.api.fees.['trading']['taker']* price, 5)


def get_adjusted_prices(price, slippage):
    adj_sell_price = price *(1-slippage)
    adj_buy_price = price * (1+slippage)
    return  adj_sell_price, adj_buy_price

def initialize(context):
    # get tickers
    context.bittrex = context.exchanges['bitfinex']  # needed to be defined in the run algorithm exchange names
    context.poloniex = context.exchanges['poloniex']

    context.bittrex_trading_pair = symbol('eth_btc', context.bittrex.name)  # get conversion from etherium to bitcoin
    context.poloniex_trading_pair = symbol('eth_btc', context.poloniex.name)


def handle_data(context, data):
    # get price data from tickers
    poloniex_price = data.current(context.poloniex_trading_pair, 'price')
    bittrex_price = data.current(context.bittrex_trading_pair, 'price')

    print('Data: {}'.format(data.current_dt))
    print('Poloniex: {}'.format(poloniex_price))
    print('Bittrex: {}'.format(bittrex_price))

    # base algo need implement slippage execution time etc, assumes you have a float of currency on both exchanges
    # this avoids having to send your coins between exchanges which is a large time delay
    if(poloniex_price > bittrex_price):
        print("buy on bittrex, sell on poloniex")
        order(asset=context.bittrex_trading_pair,
              amount=1,
              limit_price=context.bittrex_price)
        order(asset=context.poloniex_trading_pair,
              amount=-1,
              limit_price=poloniex_price)
    elif(bittrex_price > poloniex_price):
        print("buy on bittrex, sell on poloniex")
        order(asset=context.bittrex_trading_pair,
              amount=-1,
              limit_price=context.bittrex_price)
        order(asset=context.poloniex_trading_pair,
              amount=1,
              limit_price=poloniex_price)

def analyze(context):
    pass



run_algorithm(initalize=initialize,
              handle_data=handle_data,
              analyze=analyze,
              capital_base=100,
              live=False,
              base_currency='btc',
              exchange_name='bitfenex, poloniex',
              data_frequency='minute',
              start=pd.to_datetime('2017-12-12', utc=True),
              end=pd.to_datetime('2017-12-13', utc=True))