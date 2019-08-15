import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
#    client.subscribe("app/#")
    client.subscribe("#")

def on_message(client, userdata, msg):
    from app.models import TestMessage
    #print("wtf")
    #print(msg.topic+" "+msg.payload.decode("utf-8"))
    #print(type(msg.payload.decode("utf-8")))
    #str_payload=msg.payload.decode("utf-8")
    #print(str_payload)
    de_payload=json.loads(msg.payload.decode("utf-8"))
    print(dict(de_payload))
    #de_payload=dict(msg.payload.decode("utf-8"))
    print("Start rpi "+msg.topic+" to client "+str(de_payload["client"])+" for "+str(de_payload["payment"]))

    #data = msg.topic+" "+str(msg.payload)
    #t = TestMessage.objects.create(data=data)

client = mqtt.Client()
client.username_pw_set(username="test_user",password="righT_pas$w0rd")
client.on_connect = on_connect
client.on_message = on_message

client.connect("m24.cloudmqtt.com", 13932, 60)