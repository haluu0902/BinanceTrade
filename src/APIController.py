from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
import decimal


class Controller():
    def __init__(self, path):
        apiKey, apiSecret = open(path,'r').read().replace('\n','').split('|')
        self.client = Client(apiKey, apiSecret)

    def GetAllPairs(self):
        raw = self.client.get_margin_all_pairs()
        pairs = []
        for r in raw:
            pairs.append(r["symbol"])
        return pairs

    def GetIntervals(self):
        times = ['1m', '3m', '5m','15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        return times
    
    def GetPriceBuyAndSell(self, pair, interval):
        if 'm' in interval:
            timeEnd = str(int(interval.replace('m',''))*2)+" minutes ago UTC"
        elif 'h' in interval:
            timeEnd = str(int(interval.replace('h',''))*2)+" hours ago UTC"
        elif 'd' in interval:
            timeEnd = str(int(interval.replace('d',''))*2)+" days ago UTC"
        elif 'w' in interval:
            timeEnd = str(int(interval.replace('w',''))*2)+" weeks ago UTC"
        elif 'M' in interval:
            timeEnd = str(int(interval.replace('M',''))*2)+" months ago UTC"
        raw = self.client.get_historical_klines(pair, interval, timeEnd)
        sellPrice = raw[0][4]
        buyPrice = raw[-1][4]
        return float(buyPrice), float(sellPrice)

    def GetDecimal(self, pair):
        info = self.client.get_symbol_info(pair)
        d = decimal.Decimal(str(float(info['filters'][2]['minQty'])))
        return d.as_tuple().exponent*-1

    def CreateOrder(self, pair, side, amount, price):
        # SIDE_BUY = 'BUY'
        # SIDE_SELL = 'SELL'
        orderStatus = True
        roundValue = self.GetDecimal(pair)
        order = self.client.create_order(
            symbol=pair,
            side=side,#SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_FOK,
            quantity=round(amount,roundValue),
            price=price)

        # _status = order.get('status')
        # if _status == 'FILLED':
        #     orderStatus = False
        #     print(orderStatus)
        # elif _status == 'EXPIRED':
        #     orderStatus = True
        return order