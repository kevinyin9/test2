from array import array
from woo.utils import sign
from .client import Client
from .consts import *
import json

from woo import client

class RestAPI(Client):

    def __init__(self, api_key, api_seceret_key):
        Client.__init__(self, api_key, api_seceret_key)

    # def test(self):
    #     return self._request(POST, '/v1/order', {}, {})

    #qurey a symbol and precision by symbol name
    def get_symbol(self, symbol):
        query = {}
        query['symbol'] = symbol
        return self._request(GET, REST_SYMBOL, query=query, signed=False)
    
    #qurey all symbols and precision
    def get_symbols(self):
        return self._request(GET, REST_SYMBOLS, query={}, signed=False)

    #qurey market price by symbol name, and the numbers of trades (optional)
    def get_market_trade(self, symbol, limit=None):
        query = {}
        query['symbol'] = symbol.upper()
        if limit:
            query['limit'] = limit
        return self._request(GET, REST_MARKET, query=query, signed=False, queryForm=True)

    def get_avail_tokens(self):
        return self._request(GET, REST_AVAIL_TOKENS, signed=False)
    
    # create order
    # order_type = LIMIT/MARKET/IOC/FOK/POST_ONLY/LIQUIDATE
    # side = SELL/BUY
    # order_price is required except order_type = MARKET
    def send_order(self, symbol, order_type, side, order_quantity=None, order_price=None, client_order_id=0, order_tag='default', order_amount=None, visible_quantity=None):
        params = {}
        params['symbol'] = symbol
        params['order_type'] = order_type.upper()
        params['side'] = side.upper()
        if order_quantity:
            params['order_quantity'] = order_quantity
        if order_price:
            params['order_price'] = order_price
        if order_amount:
            params['order_amount'] = order_amount
        if client_order_id:
            params['client_order_id'] = client_order_id
        if order_tag:
            params['order_tag'] = order_tag
        if visible_quantity:
            params['visible_quatity'] = visible_quantity if visible_quantity else order_quantity

        return self._request(POST, REST_SEND_ORDER, params=params)

    # cancel order by order_id
    def cancel_order(self, order_id, symbol):
        params = {}
        params['order_id'] = order_id
        params['symbol'] = symbol
        return self._request(DELETE, REST_CANCEL_ORDER, params=params)

    # cancel all order by symbol
    def cancel_order_all(self, symbol):
        params = {}
        params['symbol'] = symbol
        return self._request(DELETE, REST_CANCEL_ORDERS, params=params)
    
    # get order by id
    def get_order(self, oid):
        return self._request(GET, REST_GET_ORDER+str(oid))

    # get order by symbol
    def get_orders_symbol(self, symbol):
        param = {'symbol': symbol}
        return self._request(GET, REST_GET_ORDERS, params=param)
    
    # get orderbook by symbol
    def get_orderbook(self, symbol, level=None):
        query = {}
        if level:
            query['max_level'] = level
        return self._request(GET, REST_ORDERBOOK+symbol, query=query, queryForm=True)

    # get trade by id
    def get_trade(self, tid):
        return self._request(GET, REST_GET_TRADE+str(tid))

    def get_trades(self, symbol=None, order_tag=None, start_t=None, end_t=None, page=None):
        params={}
        if symbol:
            params['symbol'] = symbol
        if order_tag:
            params['order_tag'] = order_tag
        if start_t:
            params['start_t'] = start_t
        if end_t:
            params['end_t'] = end_t
        if page:
            params['page'] = page

        return self._request(GET, REST_GET_TRADES, params=params)

    def get_order_by_clientId(self, client_id):
        query = { 'client_order_id': client_id }
        return self._request(GET, REST_GET_ORDER_CLIENT+str(client_id))

    def get_holding(self):
        return self._request(GET, REST_HOLDING)

    # query account balance
    def get_account(self):
        return self._request(GET, REST_ACCOUNT)

    # status: NEW / COMPLETED / CANCELED
    def get_settlement(self, status=None, page=None):
        params = {}
        if status:
            params['status'] = status.upper()
        if page:
            params['page'] = page
        return self._request(GET, REST_GET_SETTLEMENT, params=params)

    def send_settlement(self, token, quantity, comment=None):
        params = {}
        params['settlement_token'] = token
        params['settlement_quantity'] = quantity
        if comment:
            params['comment'] = comment
        return self._request(POST, REST_SEND_SETTLEMENT, params=params)

    def get_deposit_address(self, token):
        query = { 'token': token }
        return self._request(GET, REST_GET_DEPOSIT_ADD, query=query, queryForm=True)

    # extra: address extra information such as MEMO or TAG
    # code: th eotpauth 2FA code if you bound
    def send_withdraw(self, token, to_address, amount, extra=None, code=None):
        params = {
            'token': token,
            'address': to_address,
            'amount': amount
        }
        if extra:
            params['extra'] = extra
        if code:
            params['code'] = code
        return self._request(POST, REST_SEND_WITHDROW, params=params)
    
    def cancel_withdraw(self, id):
        params = { 'id': id }
        return self._request(DELETE, REST_CANCEL_WITHDROW, params=params)

    # type: BALANCE / COLLATERAL
    # token_side: DEPOSIT / WITHDRAW
    # status: NEW / CONFIRMING / PROCESSING / COMPLETED / CANCELED
    def get_asset_history(self, token=None, balance_token=None, type=None, token_side=None, status=None, start_t=None, end_t=None, page=None):
        params={}
        if token:
            params['token'] = token
        if balance_token:
            params['balance_token'] = balance_token
        if type:
            params['type'] = type.upper()
        if token_side:
            params['token_side'] = token_side.upper()
        if status:
            params['status'] = status.upper()
        if start_t:
            params['start_t'] = start_t
        if end_t:
            params['end_t'] = end_t
        if page:
            params['page'] = page

        return self._request(GET, REST_GET_ASSET_HISTORY, params=params)

    def get_transfer_history(self, start_t=None, end_t=None, page=None):
        params = {}
        if start_t:
            params['start_t'] = start_t
        if end_t:
            params['end_t'] = end_t
        if page:
            params['page'] = page
        return self._request(GET, REST_GET_TRANSFER_HISTORY, params=params)

    # side: LOAN / REPAY
    def get_interst_history(self, token=None, side=None, start_t=None, end_t=None, page=None):
        params = {}
        if token:
            params['token'] = token
        if side:
            params['side'] = side.upper()
        if start_t:
            params['start_t'] = start_t
        if end_t:
            params['end_t'] = end_t
        if page:
            params['page'] = page
        return self._request(GET, REST_GET_INTEREST_HISTORY, params=params)
    
    def repay_interest(self, token, amount):
        params = {
            'token': token,
            'amount': amount
        }
        return self._request(POST, REST_REPAY_INTEREST, params=params)
#----------------------------------------------

##########################################



    # query all order
    # side: BUY/SELL
    # order_type: LIMIT/MARKET/IOC/FOK/POST_ONLY/LIQUIDATE
    # order_tag: AN optional tag for this order
    # 
    def get_all_order(self, symbol=None, side=None, order_type=None, order_tag=None, startdate=None, enddate=None, pagesize=None, page=None, sort=None):
        params = {}
        if symbol:
            params['symbol'] = symbol
        if startdate:
            params['startDate'] = startdate
        if enddate:
            params['endDate'] = enddate
        if pagesize:
            params['pageSize'] = pagesize
        if page:
            params['page'] = page
        if sort:
            params['sort'] = sort
        return self._request_with_params(GET, REST_ALL_ORDER, params)

    #query all trade
    def get_all_trade(self, symbol, startdate=None, enddate=None, pagesize=None, page=None, sort=None):
        params = {}
        params['symbol'] = symbol
        if startdate:
            params['startDate'] = startdate
        if enddate:
            params['endDate'] = enddate
        if pagesize:
            params['pageSize'] = pagesize
        if page:
            params['page'] = page
        if sort:
            params['sort'] = sort
        return self._request_with_params(GET, REST_ALL_TRADE, params)

    #qurey all symbol ticker
    def get_all_ticker(self):
        params = {}
        return self._request_no_sign_params(GET, REST_ALL_TICKER, params)

    #qurey k-line records
    def get_records(self, symbol, period):
        params = {}
        params['symbol'] = symbol
        params['period'] = period
        return self._request_no_sign_params(GET, REST_RECORDS, params)

    #qurey ticker by symbol
    def get_ticker(self, symbol):
        params = {}
        params['symbol'] = symbol
        return self._request_no_sign_params(GET, REST_TICKER, params)

    #qurey the latest transaction price of each symbol of currencies
    def get_market(self):
        params = {}
        return self._request_no_sign_params(GET, REST_MARKET, params)

    #qurey the depth of buying and selling
    def get_market_dept(self, symbol, type):
        params = {}
        params['symbol'] = symbol
        params['type'] = type
        return self._request_with_params(GET, REST_DEPTH, params)

    #mass create and cancel order
    # params example:{'btcusdt',
    # cancel_orders=[1,12,31,234],
    # create_orders=[{'side':'buy', 'type':'market', 'volume':1000},{'side':'buy', 'type':'limit', 'volume':1.5, 'price':10000}]}
    def create_and_cancel_mass_orders(self, symbol, create_orders=None, cancel_orders=None):
        params = {}
        if cancel_orders:
            params['mass_cancel'] = json.dumps(cancel_orders)
        if create_orders:
            request_params = []
            for param in create_orders:
                param['side'] = param['side'].upper()
                param['type'] = '1' if (param['type'] == 'limit') else '2'
                request_params.append(param)
            params['mass_place'] = json.dumps(request_params)
        params['symbol'] = symbol
        return self._request_with_params(POST, REST_MASS_REPLACE, params)

    #qurey the current order(including uncompleted and ongoing order)
    def get_new_order(self, symbol, pagesize=None, page=None):
        params = {}
        params['symbol'] = symbol
        if pagesize:
            params['pageSize'] = pagesize
        if page:
            params['page'] = page
        return self._request_with_params(GET, REST_NEW_ORDER, params)

    #qurey order details by order_id
    def get_order_info(self, id, symbol):
        params = {}
        params['order_id'] = id
        params['symbol'] = symbol
        return self._request_with_params(GET, REST_ORDER_INFO, params)

