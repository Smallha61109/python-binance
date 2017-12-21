
class BinanceAPIException(Exception):

  def __init__(self, res):
    print(res.status_code)

class BinanceInvalidResponseException(Exception):

  def __init__(self, res):
    print(res.text)
