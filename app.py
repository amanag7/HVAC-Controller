from flask import Flask, render_template,request,flash
import paho.mqtt.client as mqttClient
import time
import random
import math
import sys

def on_connect(client,userdata, flags, rc):
	if rc == 0:
		print("Connect to broker")
	else:
		print("Connection failed Return Code : ",rc)

heating = 0
ac = 21
ventilation = 0
received_temp = 30

headings=("Room Temperature","Heating Level","Ventilation Level","AC temperature")
data = list((received_temp,heating,ventilation,ac))
ambient_temp = 21   #default
		
def on_message(client, userdata, message):
    global ac, ventilation, heating, received_temp,data
    ac = int(message.payload.split()[0])
    heating = int(message.payload.split()[1])
    ventilation = int(message.payload.split()[2])
    received_temp = int(message.payload.split()[3])
    data = list((received_temp,heating,ventilation,ac))
    print("Received Temperature from Sensor: " + str(received_temp) + "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation) + "\n")

client_name = "user-display"
broker_address = "127.0.0.1"
broker_port = 1883
user = "admin"
password = "hivemq"

client = mqttClient.Client(client_name)
client.on_connect = on_connect
client.on_message = on_message
client.connect(host = broker_address, port = broker_port)
client.subscribe('temperature/Controller')

print(client_name)
client.loop_start()

app = Flask(__name__)
app.secret_key = "iot_project"




def index():
    global ambient_temp
    if request.method == "POST":
        ambient_temp = request.form['temperature_ip']
        client.publish('temperature/' + client_name, ambient_temp)
        flash(str(ambient_temp))
    return render_template("index.html",headings=headings,data=data,ambient_temp=ambient_temp)
app.add_url_rule("/",view_func=index,methods=["POST","GET"])

if __name__ == "__main__":
    app.run()
