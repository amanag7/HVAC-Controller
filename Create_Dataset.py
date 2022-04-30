# Our dataset will consists of 1000 rows. And the columns will be [Room_Temperature, Ambient_Temperature, AC, Heating, Ventilation]

import random
import numpy as np
import pandas as pd
import math

n = 10000
room_temp = np.random.randint(10, 40, size=n)
ambient_temp = np.random.randint(18,25, size = n)

ac_list = []
heating_list = []
ventilation_list = []

ac = 21
heating = 0
ventilation = 0

for i in range(n):
    
    diff = abs(room_temp[i] - ambient_temp[i])
    #Handling the case when reveived temp from the sensor is less than ambient temperature
    
    if room_temp[i] < ambient_temp[i]:
        ac += math.ceil(diff/8)
        heating += math.ceil(diff/5)
        #loops for controlling the overflow of range
        if heating >= 5:
            heating = 4
        if ac > 26:
            ac = 26
        if diff >= 1 and diff < 5:
            ventilation = 3
        elif diff >=5 and diff < 8:
            ventilation = 2
        elif diff >=8 and diff < 12:
            ventilation = 1
        else:
            ventilation = 0
            
    #Handling the case when reveived temp from the sensor is greater than ambient temperature
    elif room_temp[i] > ambient_temp[i]:
        ac -=  math.ceil(diff/8)
        heating -= math.ceil(diff/5)
        #loops for controlling the underflow of range
        if heating < 0:
            heating = 1
        if ac < 16:
            ac = 16
        if diff >= 1 and diff < 5:
            ventilation = 3
        elif diff >=5 and diff < 8:
            ventilation = 2
        elif diff >=8 and diff < 12:
            ventilation = 1
        else:
            ventilation = 0
    else:
        pass

    ac_list.append(ac)
    heating_list.append(heating)
    ventilation_list.append(ventilation)
    
data = {'Room Temperature' : room_temp, 'Ambient Temperature' : ambient_temp, 'AC' : ac_list, 'Heating': heating_list, 'Ventilation': ventilation_list}
df = pd.DataFrame(data)

df.to_csv("dataset.csv",index=False)
