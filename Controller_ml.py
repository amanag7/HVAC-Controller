import paho.mqtt.client as mqttClient
import time
import math
import random
import pickle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

#default values for ac,ventilation,heating,ambient temperature
ambient_temperature = 21
ac = 21
heating = 0
ventilation = 0

ventil_flag=0
to_be_sent=""
received_humid = 40
received_temp = 25

df = pd.read_csv("dataset.csv")
X = df[['Room Temperature', 'Ambient Temperature']].to_numpy()
y_ac = df['AC'].to_numpy()
y_heat = df['Heating'].to_numpy()
y_vent = df['Ventilation'].to_numpy()
    
model_ac = RandomForestClassifier()
model_ac.fit(X, y_ac)
    
model_heat = RandomForestClassifier()
model_heat.fit(X, y_heat)
    
model_vent = RandomForestClassifier()
model_vent.fit(X, y_vent)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        print('\n')
    else:
        print("Connection failed Return Code : ",rc)

def on_message(client, userdata, message):
    global to_be_sent, heating, ac, ventilation, received_temp, ambient_temperature, received_humid
 
    if message.topic.split('/')[0] == 'temperature':
        received_temp = int(message.payload)
    else:
        received_humid = int(message.payload)
 
    print("Received Temperature from Sensor: " + str(received_temp))
    print("Received % Humidity from Sensor: " + str(received_humid))


    ac = model_ac.predict([[received_temp,ambient_temperature]])[0]
    heating = model_heat.predict([[received_temp,ambient_temperature]])[0]
    if ventil_flag==1:
        ventilation = ventilation
    else:
        ventilation = model_vent.predict([[received_temp,ambient_temperature]])[0]

    #to_be_sent : message containing ac, heating, ventilation, and received temperature
    to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp)+ " " + str(received_humid)
    to_be_disp = "Received Temperature from Sensor: " + str(received_temp) + " Received Humidity from Sensor: " + str(received_humid) +"  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation)
    print(to_be_disp)
    print("Ambient Temp:",ambient_temperature)
    print('\n')

#function for taking the value of ambient temperature, if user want to change the ambient temperature
def temperature_to_set(client, userdata, message):
    global ambient_temperature, to_be_sent, heating, ac, ventilation, received_temp, received_humid, ventil_flag
    if message.topic.split('/')[0] == 'temperature':
        ambient_temperature = int(message.payload)
    else:
        ventilation = int(message.payload)
        if ventilation!=-1:
            ventil_flag=1
        else:
            ventil_flag=0
    print("Received Temperature from Sensor: " + str(received_temp))

    ac = model_ac.predict([[received_temp,ambient_temperature]])[0]
    heating = model_heat.predict([[received_temp,ambient_temperature]])[0]
    if ventil_flag==1:
        ventilation = ventilation
    else:
        ventilation = model_vent.predict([[received_temp,ambient_temperature]])[0]

    #to_be_sent : message containing ac, heating, ventilation, and received temperature
    to_be_disp = "Received Temperature from Sensor: " + str(received_temp) + " Received Humidity from Sensor: " + str(received_humid) + "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation)
    to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp)+ " " + str(received_humid)
    print(to_be_disp)
    print("Ambient Temp:",ambient_temperature)
    print('\n')

client_name = "Controller" #client name
broker_address = "127.0.0.1"  # Broker address
broker_port = 1883  # Broker port
user = "admin"
password = "hivemq"

client = mqttClient.Client(client_name)  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message
client.message_callback_add('temperature/user-display',temperature_to_set)
client.message_callback_add('humidity/user-display',temperature_to_set)
client.connect(host=broker_address, port=broker_port)
client.subscribe('temperature/Room_temp_sensor') #channel for receiving the temperature from temperature sensor
client.subscribe('humidity/Room_humidity_sensor') #channel for receiving the % humidity from humidity sensor
client.subscribe('temperature/user-display') #channel for receiving temperature from the user
client.subscribe('humidity/user-display') #channel for receiving ventilation from the user
print(client_name)

client.loop_start()
time.sleep(5)

#log_file_ml.txt will contain all the changes gone  through the execution of the code
f =  open("log_file_ml.txt", "w") #log_file_ml.txt will save the log files

received_temp = random.randint(18, 25)
print("Received Temp from Sensor: " + str(received_temp))
to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp)+ " " + str(received_humid)
to_be_disp = "Received Temperature from Sensor: " + str(received_temp) +" Received Humidity from Sensor: " + str(received_humid)+ "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation)
print(to_be_disp)
print("Ambient Temp:",ambient_temperature)
print('\n')

end_time=time.time() + 300
while time.time() < end_time:
    client.publish('temperature/' + client_name, to_be_sent)
    f.write("Received Temperature from Sensor: " + str(received_temp) +" Received Humidity from Sensor: " + str(received_humid)+ "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation) + "\n")
    time.sleep(3)   

f.close()
print("exiting")
