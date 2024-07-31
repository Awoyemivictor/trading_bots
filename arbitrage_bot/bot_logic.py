import os
from dotenv import load_dotenv
from binance.spot import Spot
from pybit.unified_trading import HTTP
import time
import json
import logging

# Set up logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO)

# Loading enviroment variables
load_dotenv()

# Binance credentials
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Bybit credentials
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")


# Initialize Binance Client
binance_client = Spot(BINANCE_API_KEY, BINANCE_SECRET_KEY,
                      base_url="https://testnet.binance.vision")
# Initialize Bybit Client
bybit_client = HTTP(testnet=True, api_key=BYBIT_API_KEY,
                    api_secret=BYBIT_SECRET_KEY)


# Define trading parameters
TRADE_AMOUNT = 0.01 # Adjust based on capital and risk tolerance
STOP_LOSS_PERCENT = 0.01 # 1% stop loss
TAKE_PROFIT_PERCENT = 0.02 # 2% take profit

# Function to fetch price of a symbol from Binance
def get_binance_price(symbol):
    try:
        ticker = binance_client.ticker_price(symbol)
        return float(ticker['price'])
    except Exception as e:
        print(f"Error fetching price from Binance for {symbol}: {e}")
        return None

# Function to fetch price of a symbol from Bybit


def get_bybit_price(symbol):
    try:
        ticker = bybit_client.get_tickers(
            category="spot", symbol="BTCUSDT")
        return float(ticker['result']['list'][0]['usdIndexPrice'])
    except Exception as e:
        print(f"Error fetching price from Bybit for {symbol}: {e}")
        return None


# Function to execute trade
def execute_trade(exchange, symbol, side, quantity):
    try:
        if exchange == 'binance':
            if side == 'buy':
                response = binance_client.new_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)
            elif side == 'sell':
                response = binance_client.new_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)
        elif exchange == 'bybit':
            if side == 'buy':
                response = bybit_client.place_order(category='spot', symbol=symbol, side='Buy', orderType='Market', qty=quantity)
            elif side == 'sell':
                response = bybit_client.place_order(category='spot', symbol=symbol, side='Sell', orderType='Market', qty=quantity)
        logging.info(f"Executed {side} order on {exchange} for {quantity} {symbol}")
    except Exception as e:
        logging.error(f"Error executing trade on {exchange}: {e}")

# Function to check arbitrage opportunity between Binance or Bybit
def check_artbitrage_opportunity(symbol):
    messages = []
    messages.append(f"Checking arbitrage opportunity for {symbol}")
    binance_price = get_binance_price(symbol)
    bybit_price = get_bybit_price(symbol)

    if binance_price is None or bybit_price is None:
        messages.append("Error fetching prices.")
        return "\n".join(messages)

    messages.append(f"Binance Price: {binance_price}, Bybit Price: {bybit_price}")

    if binance_price < bybit_price:
        messages.append(f"Arbitrage Opportunity: Buy on Binance at {binance_price} and sell on Bybit at {bybit_price}")
        try:
            execute_trade('binance', symbol, 'buy', TRADE_AMOUNT)
            execute_trade('bybit', symbol, 'sell', TRADE_AMOUNT)
            messages.append(f"Executed: Buy on Binance, Sell on Bybit.")
        except Exception as e:
            messages.append(f"Error executing trade: {str(e)}")
    elif bybit_price < binance_price:
        messages.append(f"Arbitrage Opportunity: Buy on Bybit at {bybit_price} and sell on Binance at {binance_price}")
        try:
            execute_trade('bybit', symbol, 'buy', TRADE_AMOUNT)
            execute_trade('binance', symbol, 'sell', TRADE_AMOUNT)
            messages.append(f"Executed: Buy on Bybit, Sell on Binance.")
        except Exception as e:
            messages.append(f"Error executing trade: {str(e)}")
    else:
        messages.append("No arbitrage opportunity found.")
    
    return "\n".join(messages)


def main():
    while True:
        symbol = 'BTCUSDT'  # Ensure the ticker is correct for both platforms
        check_artbitrage_opportunity(symbol)
        time.sleep(60)  # Sleep to manage rate limits


if __name__ == "__main__":
    main()
