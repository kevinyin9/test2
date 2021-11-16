import sys
sys.path.insert(0,'..')

import  websocket
from  websocket  import  create_connection
from  websocket._exceptions  import  WebSocketConnectionClosedException
import  time
import threading
import  json
import woo
import timeit
from  woo.consts  import  *
from woo.utils import *
import datetime
from datetime import date
from getpass import getpass
import threading
import time
import pandas as pd

#from mysql.connector import connect, Error
from csv_process import to_csv, write, get_lists, init, raw_data_df
with open('../config.json') as json_file:
    config = json.load(json_file)

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
    api.orderbook_update(ws, id='book', sub=True, symbol='SPOT_AXS_USDT')

crawl_first_data = True
old_bids = []
old_asks = []
write_ctr = 1

csv_bids = []
csv_asks = []
csv_since = []

data = {'timestamp': [], 'data':[]}
res = pd.DataFrame(data)

'''
def insert_new_data(cur_data, old_data, key, t):
    try:
        mydb = connect(
            host=config["db_host"],
            user=config["db_user"],
            password=config["db_pwd"],
            database=config["database"]["woo_socket"]
        )
    except Error as e:
        print(e)
    cur = mydb.cursor(buffered=True)
    for data in cur_data:
        if data in old_data:
            continue
        else:
            ts = int(t)
            since = str(datetime.datetime.fromtimestamp(ts
            (price, size) = data
            find_exist = "SELECT id FROM orderbook_{0} WHERE price='{1}' AND quantity='{2}';".format(key, price, size)
            cur.execute(find_exist)
            result = cur.fetchone()
            if (not result):
                try:
                    sql = "INSERT INTO orderbook_{0} (price, quantity, time) VALUES ('{1}', '{2}', '{3}' )".format(key, price, size, since)
                    cur.execute(sql)
                except:
                    print("Fail to insert data")
    
    mydb.commit()
    cur.close()
    mydb.close()
'''
    

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

pools = []

def on_message ( ws , message ):
    global old_asks
    global old_bids
    global write_ctr
    global crawl_first_data
    global df
    global pools
    msg = json.loads(message)

    if  'ping' in message:
        ts  =  get_timestamp()
        api.pong(ws, ts)
        print("  send pong back")
    else :
        tmp_old_asks = old_asks.copy()
        tmp_old_bids = old_bids.copy()
        #t = threading.Thread(target = insert_new_data,  args=[msg["data"]["asks"], tmp_old_asks, "asks", msg["ts"]])
        #t2 = threading.Thread(target = insert_new_data,  args=[msg["data"]["bids"], tmp_old_bids, "bids", msg["ts"]])
        #t.start()
        #t2.start()
        #pools.append((t, t2))
        save_time(msg["ts"])
        save_data(msg["data"]["asks"], "asks")
        save_data(msg["data"]["bids"], "bids")
        if(write_ctr == 10):
            tmp_ask = csv_asks.copy()
            tmp_bids = csv_bids.copy()
            tmp_times = csv_since.copy()
            write(tmp_ask, tmp_bids, tmp_times)
            csv_asks.clear()
            csv_bids.clear()
            csv_since.clear()
            write_ctr = 0
            crawl_first_data = True
            '''
            for (t, t2) in pools:
                t.join()
                t2.join()
            pools.clear()
            '''

        old_asks = msg["data"]["asks"].copy()
        old_bids = msg["data"]["bids"].copy()
        # t.join()
        # t2.join()
        write_ctr+=1
if  __name__  ==  '__main__' :
    init()
    ws  =  websocket.WebSocketApp ( WS_URL ,
                                on_message = on_message ,
                                on_error = on_error ,
                                on_close = on_close ,
                                on_open = on_open )
    ws.run_forever ()
