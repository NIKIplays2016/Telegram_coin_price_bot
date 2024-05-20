import okx.MarketData as MarketData

def get_price():
    marketDataAPI = MarketData.MarketAPI(flag="0")
    result = marketDataAPI.get_orderbook(
        instId="NOT-USDT"
    )
    return {"buy": result["data"][0]["asks"][0][0], "sell": result["data"][0]["bids"][0][0]}