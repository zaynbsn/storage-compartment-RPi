import websocket
from threading import Thread

class ClientWS:
  def __init__(self, url):
    self.url = url
    self.ws = websocket.WebSocketApp(self.url,
                              on_open = self.__on_open,
                              on_message = self.__on_message,
                              on_error = self.__on_error,
                              on_close = self.__on_close)
    self.isConnected = False

  def addMessageFunction(self, function):
    self.displayMessageInTkinter = function

  def sendMessage(self, message):
    if self.isConnected:
      self.ws.send(message)
      return True
    else:
      return False

  def start(self):
    websocket.enableTrace(True)
    thread = Thread(target=self.ws.run_forever)
    thread.start()

  def __on_message(self, ws, message):
    print('FROM on_message clientWS')
    print(message)

  def __on_error(self, ws, error):
      print(error)

  def __on_close(self, ws, close_status_code, close_msg):
      print("### closed ###")
      self.isConnected = False

  def __on_open(self, ws):
      print("Opened connection")
      self.isConnected = True