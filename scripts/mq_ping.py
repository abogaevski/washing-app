import os
from datetime import datetime

now = datetime.now()
timestamp = str(datetime.timestamp(now)).split(".")[0]
message = str('{"date": "'  + str(timestamp) + '"}')

os.system('mosquitto_pub -h "localhost" -t "02421B5AB1F2/rpi_ping" -u mqttuser -P Uwxd_D41 -q 2 -m \'{}\''.format(message))