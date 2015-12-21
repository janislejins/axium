from requests_futures.sessions import FuturesSession
from random import randint
session = FuturesSession()
payload={'u':'0','d':'125,0,125,0,0,0,0,0,0,0,0,0'}

import threading
def CheckIt():
  # print "Hello, World!"
  future_two = session.get('http://raspberrypi.local:9090/get_dmx?u=0')
  # response_two = future_two.result()
  # print(response_two.content)
  c = threading.Timer(1.0, CheckIt)
  c.daemon = True #kill the thread when you kill the program
  c.start()

CheckIt()
Channel = ['0','0','0','0','0','0','0','0','0','0','0','0','0']
def ChangeIt():
	Channel[0] = str(randint(220,255))
	Channel[2] = str(randint(220,255))
	Channel[5] = '255'
	Channel[7] = str(randint(0,255))
	Channel[8] = str(randint(0,255))
	Channel[9] = str(randint(0,255))
	Channel[10] = str(randint(0,255))
	print('moved')
	myString = ",".join(Channel)
	payload={'u':'0','d': myString}
	future_one = session.post("http://raspberrypi.local:9090/set_dmx", data=payload)
	d = threading.Timer(5.0, ChangeIt)
	d.daemon = True
	d.start()
# print('response one status: {0}'.format(response_one.status_code))
ChangeIt()

# first request is started in background

# wait for the second request to complete, if it hasn't already

# print('response two status: {0}'.format(response_two.status_code))
