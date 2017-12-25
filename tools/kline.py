from binance import client
from datetime import datetime, timedelta
import threading
import time
import numpy as np

class klines:
  dtype = [
      ('opentime', 'u8'),
      ('open', 'f4'),
      ('high', 'f4'),
      ('low', 'f4'),
      ('close', 'f4'),
      ('volume', 'f4'),
      ('closetime', 'u8'),
      ('quoteassetvol', 'f4'),
      ('numberoftrades', 'u4'),
      ('takerbuybase', 'f4'),
      ('takerbuyquote', 'f4')]


  class technical_analysis_line:
    data = np.empty(shape=(0),dtype=np.float32)
    data_iter = 0
    def __init__(self, name, buffer_shape):
      self.name = name
      self.data_buffer = np.zeros(buffer_shape)

    def add_data(self, d):
      for i in d:
        data_buffer = np.roll(data_buffer, 1)
        data_buffer[-1] = i
        data_iter += 1
        self.calculate()

    def calculate(self):
      pass

  class sma(technical_analysis_line):
    def __init__(self, k):
      super().__init__(self, name = 'sma_{}'.format(k), buffer_shape=(k))
      self.k = k

    def calculate(self):
      data = np.append(data, np.mean(data_buffer))

  analysis_lines = {
      'sma':[sma(5), sma(10), sma(20), sma(60), sma(60*2), sma(60*4), sma(60*8), sma(60*24)]
    }

  klines_data = np.ndarray(shape=(0), dtype=dtype)

  def __init__(self):
    self.c = client.Client()
    self.stop_event = threading.Event()
    self.update = threading.Thread(target=self._update_loop)
    self.update.daemon = True
    self.update.start()

  def _update_loop(self):
    update_time = (datetime.now() - timedelta(minutes=5)).replace(second=0)
    while True:
      now = datetime.now()
      if now - update_time > timedelta(minutes=1):
        k = self.c.klines('ETHUSDT', '1m', update_time, now)
        update_time = now
        self.klines_data = np.append(self.klines_data, np.array(
            [tuple(i[0:11]) for i in k], dtype=self.klines_data.dtype))

        self.update_sma()
      time.sleep(30)

  def update_sma(self):
    for i in self.analysis_lines['sma']:
      i.add_data(klines_data[i.data_iter:]['close'])

  def update_macd(self):
    pass

k = klines()
for i in range(5):
  print(k.klines_data)
  time.sleep(5)
