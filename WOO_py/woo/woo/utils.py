import hmac
import base64
import time
import hashlib
import collections
from . import consts as c

def keysort(dictionary):
    return collections.OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

def sign(params, api_secret, api_timestamp):
    query = keysort(params)
    keys = list(query.keys())

    message = ''
    for i in range(0, len(keys)):
        key = keys[i]
        message += (key+'=')
        message += (str(query[key])+'&')
    message = message[:-1]
    message += ('|'+str(api_timestamp))

    print('message:\n{}\n'.format(message))
    # message = '{} {} {}'.format(nonce, customer_id, api_key)

    signature = hmac.new(
        bytes(api_secret , 'latin-1'), 
        msg = bytes(message , 'latin-1'), 
        digestmod = hashlib.sha256).hexdigest().upper()
    # print(signature)

    # md = hashlib.md5()
    # # print('sign message:', message)
    # md.update((message + api_secret).encode(encoding='utf-8'))
    # msg_md5 = md.hexdigest()
    return signature

def parse_params_to_str(params):
    url = ''
    for key, value in params.items():
        url = url + str(value) + '&'
        # url = url + str(value) + '&'
    return url[0:-1]

def parse_params_to_query(params):
    url='?'
    for key, val in params.items():
        url = url + str(key) + '=' + str(val) + '&'
    return url[0:-1]

def get_header(api_key, timestamp, sign=None):
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_FORM
    header['x-api-key'] = api_key
    if sign:
        header['x-api-signature'] = sign
    header['x-api-timestamp'] = str(timestamp)
    header['cache-control'] = 'no-cache'

    return header

def get_timestamp():
    timestamp = int(time.time()*1000)
    return timestamp


def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)
