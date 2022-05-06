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
ambient_temp = 21   #default

heads1 = ("Room Temperature","Ambient temperature")
heads2=("Heating Level","Ventilation Level","AC temperature")
data1 = list((received_temp,ambient_temp))
data2 = list((heating,ventilation,ac))
		
def on_message(client, userdata, message):
    global ac, ventilation, heating, received_temp, data1, data2
    ac = int(message.payload.split()[0])
    heating = int(message.payload.split()[1])
    ventilation = int(message.payload.split()[2])
    received_temp = int(message.payload.split()[3])
    data1 = list((received_temp,ambient_temp))
    data2 = list((heating,ventilation,ac))
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
    global ambient_temp,data1, data2,ventilation
    prev_ventil = ventilation

    if request.method == "POST":
        ambient_temp = request.form.get('temperature_ip')
        ventilation = request.form.get('ventil_ip')
        if ventilation=="select_pls":
            ventilation=prev_ventil
        elif ventilation!="auto" and ventilation!="select_pls":
            ventilation = int(ventilation)
            client.publish('humidity/'+ client_name, ventilation)
        else: pass

        data1 = list((received_temp,ambient_temp))
        data2 = list((heating,ventilation,ac))

        client.publish('temperature/' + client_name, ambient_temp)

    return render_template("index.html",heads1=heads1,data1=data1,heads2=heads2,data2=data2,ambient_temp=ambient_temp)

app.add_url_rule("/",view_func=index,methods=["POST","GET"])

def auto_ambient():
    if request.method == "POST":
        state = request.form.get('state_ip')
        flash(str(state))
    return render_template("auto_ambient.html",heads1=heads1,data1=data1,heads2=heads2,data2=data2)
app.add_url_rule("/auto_ambient",view_func=auto_ambient,methods=["POST","GET"])


if __name__ == "__main__":
    app.run()
