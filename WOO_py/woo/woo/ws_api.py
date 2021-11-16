from . import consts as c, utils
import  websocket
import  gzip
import  time
import  json
from  woo.consts  import  *
import woo.utils as utils

class WsAPI:

    def __init__(self, api_key, api_secret_key):
        self.api_key = api_key
        self.api_secret_key = api_secret_key

    def req_orderbook(self,ws, id, symbol):
        print('hi req_orderbook')
        req = {
            "id": id,
            "event": "request",
            "params": {
                "type": "orderbook",
                "symbol": symbol
            }
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )

    def orderbook(self, ws, id, sub, symbol, freq=None):
        topic = "{}@orderbook100".format(symbol)
        if freq:
            topic += str(freq)
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": topic
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))

    def pong(self, ws, ts):
        req = {
            "event": "pong",
            "ts": ts
        }
        ws.send (json.dumps(req))

    def orderbook_update(self, ws, id, sub, symbol):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "{}@orderbookupdate".format(symbol)
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        # time . sleep ( 1 )        

    def trade(self, ws, id, sub, symbol):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "{}@trade".format(symbol)
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )   

    def ticker(self, ws, id, sub, symbol):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "{}@ticker".format(symbol)
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )     

    def tickers(self, ws, id, sub):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "tickers"
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )     
    
    def bbo(self, ws, id, sub, symbol):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "{}@bbo".format(symbol)
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )   

    def bbos(self, ws, id, sub):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "bbos"
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )  

    # time: 1m/5m/15m/30m/1h/1d/1w/1M
    def kline(self, ws, id, sub, symbol, time):
        req = {
            "id": id,
            "event": "subscribe" if sub else "unsubscribe",
            "topic": "{}@kline_{}".format(symbol, time)
        }
        print('send parameters:\n{}\n'.format(json.dumps(req)))
        ws.send (json.dumps(req))
        time . sleep ( 1 )    
