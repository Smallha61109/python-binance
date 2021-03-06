import hmac
import hashlib
import requests
import time
import json
from urllib.parse import urlencode
from .exceptions import BinanceAPIException, BinanceInvalidResponseException


class Client:
  API_URL = 'https://api.binance.com/api/'
  PUBLIC_API = 'v1'
  PRIVATE_API = 'v3'

  KLINE_INTERVAL_1MINUTE = '1m'
  KLINE_INTERVAL_3MINUTE = '3m'
  KLINE_INTERVAL_5MINUTE = '5m'
  KLINE_INTERVAL_15MINUTE = '15m'
  KLINE_INTERVAL_30MINUTE = '30m'
  KLINE_INTERVAL_1HOUR = '1h'
  KLINE_INTERVAL_2HOUR = '2h'
  KLINE_INTERVAL_4HOUR = '4h'
  KLINE_INTERVAL_6HOUR = '6h'
  KLINE_INTERVAL_8HOUR = '8h'
  KLINE_INTERVAL_12HOUR = '12h'
  KLINE_INTERVAL_1DAY = '1d'
  KLINE_INTERVAL_3DAY = '3d'
  KLINE_INTERVAL_1WEEK = '1w'
  KLINE_INTERVAL_1MONTH = '1M'

  def __init__(self, api_key=None, api_secret=None):
    """Binance API Client constructor
    :param api_key: Api Key
    :type api_key: str.
    :param api_secret: Api Secret
    :type api_secret: str.
    """

    self.session = requests.session()
    headers = {'Accept': 'application/json', 'User-Agent': 'binance/python'}

    if api_key is not None and api_secret is not None:
      self.set_api_key(api_key, api_secret)
      headers['X-MBX-APIKEY'] = self.API_KEY

    self.session.headers.update(headers)

    # init DNS and SSL cert
    self.ping()

  def set_api_key(self, api_key, api_secret):
      self.API_KEY = api_key
      self.API_SECRET = api_secret.encode()

  def signature(self, data):
    return hmac.new(self.API_SECRET, msg=data.encode(),
                    digestmod=hashlib.sha256).hexdigest()

  def get_request(self, path, param={}, sign=True):
    if sign:
      param['timestamp'] = int(time.time() * 1000)
      param['signature'] = self.signature(urlencode(param))
    res = self.session.get(self.API_URL + path, params=param)
    if not 200 <= res.status_code <= 299:
      raise BinanceAPIException(res)
    try:
      return res.json()
    except ValueError:
      raise BinanceInvalidResponseException(response)

  def ping(self):
    return self.get_request('v1/ping', sign=False)

  def account_into(self):
    return self.get_request('v3/account')

  def klines(self, symbol, k, startTime, endTime):
    return self.get_request('v1/klines', param={
        'symbol': symbol,
        'interval': k,
        'startTime': int(startTime.timestamp() * 1000),
        'endTime': int(endTime.timestamp() * 1000)}, sign=False)

