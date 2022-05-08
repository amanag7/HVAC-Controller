import paho.mqtt.client as mqttClient
import time
import math

#default values for ac,ventilation,heating,ambient temperature
ambient_temperature = 21
ac = 21		# AC temperatures (16-26)
heating = 0		# Heater levels (0-4)
ventilation = 0	# Ventilation levels (0-3)

ventil_flag=0
to_be_sent=""
received_humid = 40
received_temp = 25

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

    #computing the difference between the current ambient temperature and received room temperature
    diff = abs(received_temp - ambient_temperature)

    #Handling the case when reveived temp from the sensor is less than ambient temperature
    if received_temp < ambient_temperature:
        ac += math.ceil(diff/8)
        heating += math.ceil(diff/5)
        #loops for controlling the overflow of range
        if heating > 4:
            heating = 4
        if ac > 26:
            ac = 26

        if ventil_flag==1:
            ventilation = ventilation
        elif received_humid >45 and received_humid<=50:
            ventilation = 3
        elif received_humid >40 and received_humid<=45:
            ventilation = 2
        elif received_humid >35 and received_humid<=40:
            ventilation = 1
        else:
            ventilation = 0
           
    #Handling the case when reveived temp from the sensor is greater than ambient temperature
    elif received_temp > ambient_temperature:
        ac -=  math.ceil(diff/8)
        heating -= math.ceil(diff/5)
        #loops for controlling the underflow of range
        if heating < 0:
            heating = 0
        if ac < 16:
            ac = 16

        if ventil_flag==1:
            ventilation = ventilation
        elif received_humid >45 and received_humid<=50:
            ventilation = 3
        elif received_humid >40 and received_humid<=45:
            ventilation = 2
        elif received_humid >35 and received_humid<=40:
            ventilation = 1
        else:
            ventilation = 0
    else:
        ac = 21 # default value for AC
        heating = 0 # heater switched off
        if ventil_flag:
            ventilation = ventilation
        else:
            ventilation = 0

    #to_be_sent : message containing ac, heating, ventilation, and received temperature
    to_be_disp = "Received Temperature from Sensor: " + str(received_temp) + " Received Humidity from Sensor: " + str(received_humid) + "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation)
    to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp) + " " + str(received_humid)
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

    #computing the difference between the current ambient temperature and received room temperature
    diff = abs(received_temp - ambient_temperature)

    #if the received temperature is equal to the ambient temperature, then do nothing
    if received_temp == ambient_temperature:
        ac = 21 # default value for AC
        heating = 0 # heater switched off
        ventilation = 0 # ventilation switched off

    #Handling the case when reveived temp from the sensor is less than ambient temperature
    elif received_temp < ambient_temperature:
        ac += math.ceil(diff/8)
        heating += math.ceil(diff/5)
        #loops for controlling the overflow of range
        if heating >= 5:
            heating = 4
        if ac > 26:
            ac = 26

        if ventil_flag==1:
            ventilation = ventilation
        elif received_humid >45 and received_humid<=50:
            ventilation = 3
        elif received_humid >40 and received_humid<=45:
            ventilation = 2
        elif received_humid >35 and received_humid<=40:
            ventilation = 1
        else:
            ventilation = 0

    #Handling the case when reveived temp from the sensor is greater than ambient temperature
    elif received_temp > ambient_temperature:
        ac -=  math.ceil(diff/8)
        heating -= math.ceil(diff/5)
        #loops for controlling the underflow of range
        if heating < 0:
            heating = 1
        if ac < 16:
            ac = 16

        if ventil_flag==1:
            ventilation = ventilation
        elif received_humid >45 and received_humid<=50:
            ventilation = 3
        elif received_humid >40 and received_humid<=45:
            ventilation = 2
        elif received_humid >35 and received_humid<=40:
            ventilation = 1
        else:
            ventilation = 0

    else:
        ac = 21 # default value for AC
        heating = 0 # heater switched off
        if ventil_flag:
            ventilation = ventilation
        else:
            ventilation = 0

    #to_be_sent : message containing ac, heating, ventilation, and received temperature
    to_be_disp = "Received Temperature from Sensor: " + str(received_temp) + " Received Humidity from Sensor: " + str(received_humid) + "  " + "AC: " + str(ac) + "  "+ "Heating: "+ str(heating) + "  " + "Ventilation: " + str(ventilation)
    to_be_sent = str(ac) + " " + str(heating) + " " + str(ventilation) + " " + str(received_temp) + " " + str(received_humid)
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

#output.txt will contain all the changes gone  through the execution of the code
f =  open("output.txt", "w") #output.txt will save the log files

#assuming every request will come after 10sec from the previous transaction
end_time=time.time() + 300
while time.time() < end_time:
    client.publish('temperature/' + client_name, to_be_sent)
    f.write("Received Temperature from Sensor: " + str(received_temp) + " Received Humidity from Sensor: " + str(received_humid) + "  " + "Ambient Temperature:  " + str(ambient_temperature) + "  " + "AC: " + str(ac) + "  "+ "Heating: " + str(heating) + "  " + "Ventilation: " + str(ventilation) +"\n")
    time.sleep(3)   

f.close()
print("exiting")
