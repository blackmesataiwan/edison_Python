import time
import mraa 
import datetime
import json
import os
import QIoT
import math




Temperture = mraa.Aio(0)
#Sound = mraa.Aio(0)
Rotary = mraa.Aio(1)
Light = mraa.Aio(2)
Piezo = mraa.Aio(3)

Button = mraa.Gpio(2)
Button.dir(mraa.DIR_IN)
Touch = mraa.Gpio(4)
Touch.dir(mraa.DIR_IN)

LED = mraa.Gpio(7)
LED.dir(mraa.DIR_OUT)

client = QIoT.setup('./res/resourceinfo.json', '/ssl/')


""" 
	Receive data of QIoT Suite Lite.
"""

#Setting Subscribe is use id <QIoT.subscribeofid("ID", client)>
#It will return topic name


def on_connect(client, userdata, flags, rc):
    global topic_LED
    print("Connected with result code "+str(rc))
    topic_LED = QIoT.subscribeofid("LED", client)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)
    if msg.topic == topic_LED:
    	if int(data['value']) == 1:
    		LED.write(1)
    	else:
    		LED.write(0)
    	

client.on_connect = on_connect
client.on_message = on_message


"""
	Send sensor's data to QIoT Suite Lite by Resourcetype.
"""

#It's use "resourcetypename" to sending data.
#QIoT.sendoftype("resourcetypename", value, client)

while True:
	try:	
		t = time.time()

		a = Temperture.read()
		QIoT.sendoftype("Temperature",int(1/(math.log(((1023-a)*10000/a)/10000)/3975+1/298.15)-273.15) , client)

		#QIoT.sendoftype("Sound", int(Sound.read()/1023*100), client)
		QIoT.sendoftype("Rotary", int(Rotary.read()/1023*100), client)
		QIoT.sendoftype("Piezo", 1 if (Piezo.read() > 100) else 0 , client)
		QIoT.sendoftype("Light", Light.read(), client)
		
		QIoT.sendoftype("Button", Button.read(), client)
		QIoT.sendoftype("Touch", Touch.read(), client)
		time.sleep(1)
	except Exception as e:
		print "IO ERROR"
	




