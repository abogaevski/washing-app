import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger('mqtt')

def publish_data(topic, data):
    def on_connect(client, userdata, flags, rc):
        logger.debug("[PUBLISHER]: Connected with result code "+str(rc))

    client = mqtt.Client()
#    client.username_pw_set(username='test_user', password= 'righT_pas$w0rd')
    client.username_pw_set(username="mqttuseruser",password="Uwxd_D41")
#    client.connect("m24.cloudmqtt.com", 13932, 60)
    client.connect("192.168.147.14", 1883, 60)
    client.publish(topic, payload=str(data), retain=False)
    client.disconnect()

