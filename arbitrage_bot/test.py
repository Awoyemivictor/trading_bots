from pybit.unified_trading import HTTP
import json
session = HTTP(testnet=True)
print(json.dumps(session.get_tickers(
    category="spot",
    symbol="BTCUSDT",
), indent=2))