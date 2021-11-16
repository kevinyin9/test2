import sys
sys.path.insert(0,'..')

import  websocket
from  websocket  import  create_connection
from  websocket._exceptions  import  WebSocketConnectionClosedException
import  time
import pandas as pd
import  json
import woo
from woo.utils import *
from  woo.consts  import  *
import datetime
from datetime import date
from getpass import getpass
# pip install mysql-connector-python

try :
    import  thread
except  ImportError :
    import  _thread  as  thread

api_key = 'i6FTR9fwKwbQka0FWUnVLg=='
api_secret = '2BRTTIAYCMPIHKVDCVNBVPNKXSLG'
api = woo.WsAPI(api_key=api_key,api_secret_key=api_secret)


i=0
if i==0:
    title=pd.DataFrame({'timestamp':['timestamp'],'price':['price'],'size':['size'],'isBuyerMaker':['isBuyerMaker']})
    title.to_csv('WOO_USDT_trade.csv',index=False,header=False,mode='a')
    i+=1

def  on_error ( ws , error ):
    print ( '### error ###' )
    print ( error )

def  on_close ( ws ):
    print ( "### closed ###" )

def  on_open ( ws ):
    print ( '### opened ###' )
    api.kline(ws=ws, id='123', sub=True, symbol='SPOT_WOO_USDT', time='1m')

def  on_message ( ws , message ):
    print(message)
    msg = json.loads(message)
    if  'ping' in message:
        ts  =  get_timestamp()
        api.pong(ws, ts)
        print("  send pong back")
    else :
        price = msg["data"]["price"]
        size = msg["data"]["size"]
        isBuyer = "False" if (msg["data"]["side"]=="BUY") else "True"
        ts = int(msg["ts"])
        #timestamp = str(datetime.datetime.fromtimestamp(ts / 1000.0, tz=datetime.timezone.utc)).split("+")[0].replace(":", ".")
        timestamp=ts
        df=pd.DataFrame({'timestamp':[ts],'price':[price],'size':[size],'isBuyerMaker':[isBuyer]})
        #df=pd.DataFrame({'price':[price],'size':[size],'isBuyerMaker':[isBuyer],index_col:[ts]})
        df.to_csv('WOO_USDT_trade.csv', header=False, index=False, mode="a")
        


if  __name__  ==  '__main__' :
    ws  =  websocket.WebSocketApp ( WS_URL ,
                                on_message = on_message ,
                                on_error = on_error ,
                                on_close = on_close ,
                                on_open = on_open )
    ws.run_forever ()






