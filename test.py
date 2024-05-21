import okx.MarketData as MarketData

def get_price():
    marketDataAPI = MarketData.MarketAPI(flag="0")
    result_not = marketDataAPI.get_orderbook(
        instId="TON-USDT"

    )
    result_ton = marketDataAPI.get_orderbook(
        instId="TON-USDT"

    )
    result_btc = marketDataAPI.get_orderbook(
        instId="BTC-USDT"

    )
    return result_btc, result_ton, result_not

print(get_price())