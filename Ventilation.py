import paho.mqtt.client as mqttClient
import time
import math

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Connected to broker")
		print('\n')
	else:
		print("Connection failed Return Code : ",rc)

def on_message(client, userdata, message):
	ventilation = int(message.payload.split()[2])
	print("Ventilation: " + str(ventilation))
	
client_name = "Ventilation" #client name
broker_address = "127.0.0.1"  # Broker address
broker_port = 1883  # Broker port
user = "admin"
password = "hivemq"

client = mqttClient.Client(client_name)  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.connect(host=broker_address, port=broker_port)
client.subscribe('temperature/Controller') #subscribe to this channel
print(client_name)

client.loop_start()
time.sleep(1)

end_time=time.time() + 300
while time.time() < end_time:
    time.sleep(1)   

print("exiting")
