import sys
sys.path.insert(0,'..')

import  websocket
from  websocket  import  create_connection
from  websocket._exceptions  import  WebSocketConnectionClosedException
import  time
import  json
import woo
from woo.utils import *
from  woo.consts  import  *
import datetime
from datetime import date
from getpass import getpass
# pip install mysql-connector-python
from mysql.connector import connect, Error

with open('../config.json') as json_file:
    config = json.load(json_file)

mydb = connect(
        host=config["db_host"],
        user=config["db_user"],
        password=config["db_pwd"],
        database=config["database"]["woo_socket"]
    )
''''    
try:
    mydb = connect(
        host=config["db_host"],
        user=config["db_user"],
        password=config["db_pwd"],
        database=config["database"]["woo_socket"]
    )
except Error as e:
    print(e)
    '''
cur = mydb.cursor()

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
    api.trade(ws, id='trade', sub=True, symbol='SPOT_AXS_USDT')

def  on_message ( ws , message ):
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
        timestamp=ts
        #timestamp = str(datetime.datetime.fromtimestamp(ts / 1000.0, tz=datetime.timezone.utc)).split("+")[0].replace(":", ".")
        find_exist = ('SELECT id FROM trade WHERE price=\'%s\' AND quantity=\'%s\' AND time=\'%s\' AND isBuyerMaker=\'%s\';' % (str(price), str(size), str(timestamp), str(isBuyer)))
        cur.execute(find_exist)
        result = cur.fetchone()
        if (not result):
            sql = "INSERT INTO AXStrade (time, isBuyerMaker, price, quantity) VALUES ('{timestamp}', '{isBuyer}', '{price}', '{size}');".format(timestamp=timestamp, isBuyer=isBuyer, price=price, size=size)
            try:
                cur.execute(sql)
                mydb.commit()
            except:
                # 避免存入同比資料兩次以上，所以有使用這個 unique_id 來判斷是否已經存在資料庫了
                print("Same id: "+str(timestamp))



if  __name__  ==  '__main__' :
    ws  =  websocket.WebSocketApp ( WS_URL ,
                                on_message = on_message ,
                                on_error = on_error ,
                                on_close = on_close ,
                                on_open = on_open )
    ws.run_forever ()






