#!/bin/sh
gnome-terminal -- /bin/sh -c "python3 Controller.py; read line"
gnome-terminal -- /bin/sh -c "python3 Room_temp_sensor.py; read line"
gnome-terminal -- /bin/sh -c "python3 AC.py; read line"
gnome-terminal -- /bin/sh -c "python3 Heating.py; read line"
gnome-terminal -- /bin/sh -c "python3 Ventilation.py; read line"
gnome-terminal -- /bin/sh -c "python3 app.py"
