# http header
API_URL = 'https://api.woo.network'
WS_URL = 'wss://wss.woo.network/ws/stream/c11c7854-ee1f-4590-bdaa-b8d546c67126'
CONTENT_TYPE = 'Content-Type'

ACEEPT = 'Accept'
COOKIE = 'Cookie'
LOCALE = 'Locale='

APPLICATION_FORM = 'application/x-www-form-urlencoded'

# REST API URL
REST_SYMBOL = '/v1/public/info/' # get, query
REST_SYMBOLS = '/v1/public/info' # get
REST_MARKET = '/v1/public/market_trades' # get
REST_AVAIL_TOKENS = '/v1/public/token'# get
REST_SEND_ORDER = '/v1/order' # post, parm
REST_CANCEL_ORDER = '/v1/order' # delete, parm
REST_CANCEL_ORDERS = '/v1/orders' # delete, parm
REST_GET_ORDER = '/v1/order/' # get, query
REST_GET_ORDERS = '/v1/orders' # get, (opt) parm
REST_ORDERBOOK = '/v1/orderbook/' # get, (opt) parm
REST_GET_TRADE = '/v1/client/trade/' # get, query
REST_GET_TRADES = '/v1/client/trades' # get, (opt) parm
REST_GET_ORDER_CLIENT = '/v1/client/order/' # get, query
REST_HOLDING = '/v2/client/holding' # get
REST_ACCOUNT = '/v1/client/info' # get
REST_GET_SETTLEMENT = '/v1/settlements' # get, (opt) parm
REST_SEND_SETTLEMENT = '/v1/settlement' # POST, parm
REST_GET_DEPOSIT_ADD = '/v1/asset/deposit' # GET, PARM
REST_SEND_WITHDROW = '/v1/asset/withdraw' #POST, PARM
REST_CANCEL_WITHDROW = '/v1/asset/withdraw' #DELETE, PARM
REST_GET_ASSET_HISTORY = '/v1/asset/history' #GET, (OPT) PARM
REST_GET_TRANSFER_HISTORY = '/v1/asset/transfer_history' #GET, (OPT) PARM
REST_GET_INTEREST_HISTORY = '/v1/interest/history' #GET, (OPT) PARM
REST_REPAY_INTEREST = '/v1/interest/repay' # POST PARM

# WS API
WS_TRADE_TICKER_SUB = '{"event":"sub","params":{"channel":"market_symbol_trade_ticker","cb_id":"custom string"}}'
WS_TRADE_TICKER_UNSUB = '{"event":"unsub","params":{"channel":"market_symbol_trade_ticker"}}'

WS_MARKET_DEPTH_SUB = '{"event":"sub","params":{"channel":"market_symbol_depth_steplevel","cb_id":"custom string","asks":150,"bids":150}}'
WS_MARKET_DEPTH_UNSUB = '{"event":"unsub","params":{"channel":"market_symbol_depth_steplevel","cb_id":"custom string","asks":150,"bids":150}}'

WS_MARKET_KLINE_SUB = '{"event":"sub","params":{"channel":"market_symbol_kline_period","cb_id":"custom string"}}'
WS_MARKET_KLINE_UNSUB = '{"event":"unsub","params":{"channel":"market_symbol_kline_period"}}'


# METHOD
GET = "GET"
POST = "POST"
DELETE = "DELETE"