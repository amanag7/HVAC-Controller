#!/bin/sh
gnome-terminal -- /bin/sh -c "python3 Controller_ml.py"
gnome-terminal -- /bin/sh -c "python3 Room_temp_sensor.py"
gnome-terminal -- /bin/sh -c "python3 Room_humidity_sensor.py"
gnome-terminal -- /bin/sh -c "python3 AC.py"
gnome-terminal -- /bin/sh -c "python3 Heating.py"
gnome-terminal -- /bin/sh -c "python3 Ventilation.py"
gnome-terminal -- /bin/sh -c "python3 app.py;"
