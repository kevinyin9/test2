import requests
from . import consts as c, utils
import json


class Client(object):

    def __init__(self, api_key, api_seceret_key):

        self.API_KEY = api_key
        self.API_SECRET_KEY = api_seceret_key


    def _request(self, method, request_path, params={}, query={}, signed=True, queryForm=False):
        timestamp = utils.get_timestamp()
        sign = None
        if signed:
            sign_params = {**params, **query} # combine 2 dictionaries
            sign = utils.sign(sign_params, self.API_SECRET_KEY, timestamp)

        header = utils.get_header(self.API_KEY, timestamp, sign=sign)

        # url
        query_str = utils.parse_params_to_query(query) if queryForm else utils.parse_params_to_str(query)
        request_path = request_path + query_str
        url = c.API_URL + request_path

        # sign & header
        body = params

        # send request
        response = None
        print("url:", url)
        print("\nheaders:")
        for key, val in header.items():
            print(key, ':', val)
        print("\nbody:")
        for key, val in body.items():
            print(key, ':', val)

        if method == c.GET:
            # response = requests.get(url)
            response = requests.get(url, data=body, headers=header)
        elif method == c.POST:
            # response = requests.post(url, data=body)
            response = requests.post(url, data=body, headers=header)
        elif method == c.DELETE:
            # response = requests.delete(url)
            response = requests.delete(url, data=body, headers=header)
        print('response\n{}'.format(response))

        return response.content  
        # exception handle
        # if not str(response.status_code).startswith('2'):
        #     print(response.status_code)
        #     raise response.json()

        # timestamp = 1578565539808
        # params = {
        #     "symbol": "SPOT_BTC_USDT",
        #     "order_type": "LIMIT",
        #     "order_price": 9000,
        #     "order_quantity": 0.11,
        #     "side": "BUY"
        # }
        # query = {
        #     'param1': 'val1',
        #     'param2': 'val2'
        # }

    # def _request_without_params(self, method, request_path):
    #     return self._request(method, request_path, {})

    # def _request_with_params(self, method, request_path, params, query):
    #     return self._request(method, request_path, params, query)

    # def _request_no_sign_params(self, method, request_path, params, sign_flag = False):
    #     return self._request(method, request_path, params, sign_flag)