 import requests
>>> payload={"u":"1","d":"125,0,125,0"}
>>> r = requests.post("http://raspberrypi.local:9090/set_dmx?", data=payload)
>>> payload={"u":"1","d":"125,0,0,0"}
>>> r = requests.post("http://raspberrypi.local:9090/set_dmx?", data=payload)
