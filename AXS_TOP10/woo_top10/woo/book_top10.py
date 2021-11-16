import sys
sys.path.insert(0,'..')

import  websocket
from  websocket  import  create_connection
from  websocket._exceptions  import  WebSocketConnectionClosedException
import  time
import  json
import woo
from  woo.consts  import  *
import datetime
from datetime import date
from getpass import getpass
import threading
import time
import pandas as pd
from woo.utils import *
from csv_process_top10 import to_csv, write_interval, get_lists, init_interval



try :
    import  thread
except  ImportError :
    import  _thread  as  thread

api_key = 'i6FTR9fwKwbQka0FWUnVLg=='
api_secret = '2BRTTIAYCMPIHKVDCVNBVPNKXSLG'
api = woo.WsAPI(api_key=api_key,api_secret_key=api_secret)

def  on_error ( ws , error ):
    print ( '### error ###' )
    print ( error )

def  on_close ( ws ):
    print ( "### closed ###" )

def  on_open ( ws ):
    print ( '### opened ###' )
    api.orderbook(ws, id='book', sub=True, symbol='SPOT_AXS_USDT')

crawl_first_data = True
write_ctr = 1

csv_bids = []
csv_asks = []
csv_since = []

def save_time(t):
    global csv_since
    global crawl_first_data
    ts = int(t)
    timestamp = ts
    if(crawl_first_data):
        print("... Crawl data ...")
        crawl_first_data = False
    print("  "+str(timestamp))
    csv_since.append(timestamp)

def save_data(cur_data, key):
    global csv_asks
    global csv_bids
    if(key == "asks"):
        csv_asks.append(cur_data)
    else:
        csv_bids.append(cur_data)

def on_message ( ws , message ):
    global old_asks
    global old_bids
    global write_ctr
    global crawl_first_data
    msg = json.loads(message)
    # print(msg)
    if  'event' in msg:
        ts  =  get_timestamp()
        api.pong(ws, ts)
        print("  send pong back")
    else :
        if write_ctr==1:
            save_time(msg["ts"])
            save_data(msg["data"]["asks"][0:10], "asks")
            save_data(msg["data"]["bids"][0:10], "bids")
        #if(write_ctr == 10):
            tmp_ask = csv_asks.copy()
            tmp_bids = csv_bids.copy()
            tmp_times = csv_since.copy()
            write_interval(tmp_ask, tmp_bids, tmp_times)
            
            csv_asks.clear()
            csv_bids.clear()
            csv_since.clear()
            write_ctr = 0
            crawl_first_data = True

        write_ctr+=1
if  __name__  ==  '__main__' :
    init_interval()
    ws  =  websocket.WebSocketApp ( WS_URL ,
                                on_message = on_message ,
                                on_error = on_error ,
                                on_close = on_close ,
                                on_open = on_open )
    ws.run_forever ()
