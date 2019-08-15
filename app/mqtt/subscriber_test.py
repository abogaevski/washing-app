import paho.mqtt.client as mqtt
from .publisher import publish_data
import json
from datetime import datetime
import pytz
from django.conf import settings
from app.utils import get_object_or_none
from django.core.exceptions import ValidationError, FieldError
#**xdsi*update
from decimal import *

def on_connect(client, userdata, flags, rc):
    print("Connected to localhost with result code "+str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    from app.models import Post, Card, Partner, Transaction, Station
    print('Has a message')
    print(str(msg.payload))
    

client = mqtt.Client()
client.username_pw_set(username="",password="")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)