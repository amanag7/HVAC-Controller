import paho.mqtt.client as mqttClient
import time
import random

def on_connect(client, userdata, flags, rc):
 if rc == 0:
    print("Connected to broker")
    print('\n')
 else:
    print("Connection failed Return Code : ",rc)

def on_message(client, userdata, message):
 pass
    
client_name="Room_temp_sensor" #client name
broker_address = "127.0.0.1"  # Broker address
broker_port = 1883  # Broker port
user = "admin"
password = "hivemq"   

client = mqttClient.Client(client_name)  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.connect(host=broker_address, port=broker_port)

print(client_name)	

client.loop_start()

end_time=time.time() + 300
while time.time() < end_time:
	#randomly generating temperature between 10 and 40 and sending to the controller
	rand_temp = random.randrange(10,40)
	print(" Room Temperature:",rand_temp)
	client.publish('location/' + client_name, str(rand_temp))
    	#sending room temperature every 30 second
	time.sleep(30)

print("exiting")
