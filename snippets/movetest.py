import requests
from random import randint
payload2= {'u':'0','d':'0,0,0,0,0,0,0,0,0,0,0,0'}
payload={'u':'0','d':'125,0,125,0,0,0,0,0,0,0,0,0'}
Channel = ['0','0','0','0','0','0','0','0','0','0','0','0','0']
I = 0
while True:
    if I == 0:
    	Channel[0] = str(randint(180,255))
    	Channel[2] = str(randint(180,255))
    	Channel[5] = '255'
    	Channel[7] = str(randint(0,255))
    	Channel[8] = str(randint(0,255))
    	Channel[9] = str(randint(0,255))
    	Channel[10] = str(randint(0,255))
    	myString = ",".join(Channel )
    	payload={'u':'0','d': myString}
    	print payload
    	r = requests.post("http://raspberrypi.local:9090/set_dmx", data=payload)
    	# print(r.text)
    	I = 1
    else:
    	Channel[0] = str(randint(180,255))
    	Channel[2] = str(randint(180,255))
    	Channel[5] = '255'
    	Channel[7] = str(randint(0,255))
    	Channel[8] = str(randint(0,255))
    	Channel[9] = str(randint(0,255))
    	Channel[10] = str(randint(0,255))
    	myString = ",".join(Channel )
    	payload={'u':'0','d': myString}
    	print payload
    	r = requests.post("http://raspberrypi.local:9090/set_dmx", data=payload)
    	# print(r.text)
    	I = 0
    # some python code that I want 
    # to keep on running
