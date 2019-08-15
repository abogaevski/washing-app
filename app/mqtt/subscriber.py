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
    print("Connected with result code "+str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    from app.models import Post, Card, Partner, Transaction, Station
    print('Has a message')
    print(str(msg.payload))
    payload=json.loads(msg.payload)
    topic=msg.topic.split('/')
    payload['rpi'] = topic[0]
    payload['command'] = topic[1]

    # print('Payload is: ' + str(payload))
    print('Topic is: ' + msg.topic)


    if payload["command"] == 'account_balance' or payload["command"] == 'start_washing' or payload["command"] == 'srv_ping':
        print("no action")

    elif payload["command"] == 'get_account_balance':

        print('------------------------------')
        print('Get account balance start')
        
        #- payload["rpi"]
        #- payload["client"]
        client = str(payload['client'])
        # card = Card.objects.get(data=client)
        card = get_object_or_none(Card, data=client)
        
        if card:
            print('Card is ' + str(card.data))
            client_balance = card.partner.balance
            print('Balance is ' + str(client_balance))

            #**************************
            #*******xdsi***************
            rpi=str(payload['rpi'])
            print('RPI is ' + rpi)
            post = get_object_or_none(Post, mac_uid=rpi)
            print(post.mac_uid)
            station=post.station
            print('Course is ' + str(station.course))
            #- fuction check balance and send it
            topic = payload['rpi'] + '/account_balance'
            print('Topic is ' + topic)

            #**************************
            #*******xdsi***************
            data = json.dumps({'client': payload["client"], 'balance': float(client_balance), 'course': station.course})
            print( str(data) )
            try:
                publish_data(topic, data)
                print( data )
                print('------------------------------')
            except:
                print("Can't send data for account balance")        
        else:
            print('card is not defined')
    

    # TRANSACTIONS
    elif payload["command"] == 'transaction':
        print('------------------------------')
        print('Transaction start')

        init_type = int(payload['type'])
        print('Init type is ' + str(init_type))

        rpi = str(payload['rpi'])
        # post = Post.objects.get(mac_uid=rpi)
        post = get_object_or_none(Post, mac_uid=rpi)
        if post:
            print('Post is ' + str(post.mac_uid))
            station = post.station
            print('Station is ' + station.owner)       

        timestamp = int(payload['date'])
        start_time_from_timestamp = datetime.fromtimestamp(timestamp)
        tz = pytz.timezone(settings.TIME_ZONE)
        start_time = tz.localize(start_time_from_timestamp)

        print('Start date is ' + str(start_time))


#**************************
#*******xdsi***************
        points = int(payload['points'])
        print('Points is ' + str(points))
        station = post.station
        price = points/station.course
        print('Price is ' + str(price))
        print(type(price))


        if init_type!=2:
            
            client = str(payload['client'])

            card = get_object_or_none(Card, data=client)
            if card:
                print('Card is ' + str(card))
                partner = card.partner
                print('Partner is ' + partner.name)     

            print(type(partner.balance))
            partner.balance -= Decimal(price)
            print('Partner balance after payment is ' + str(partner.balance))

            try:
                partner.save()
            except (ValidationError, FieldError) as err:
                print('Partner is not save ' + str(err))

            try:
                t = Transaction.objects.create(
                    card = card,
                    partner = partner,
                    station = station,
                    post = post,
                    start_time = start_time,
                    price = price,
                    initiator_type = init_type
                )
                print(t)
            except:
                print('Transaction not created HERE!')
                print('------------------------------')


        try:
            t = Transaction.objects.create(
                station = station,
                post = post,
                start_time = start_time,
                price = price,
                initiator_type = init_type
            )
            print(t)
        except:
            print('Transaction not created')
            print('------------------------------')
                
                

        
        # if t:
        #     print('Transaction is ' + str(t.start_time))
        #     print('------------------------------')
        # else:
        #     print('Transaction not created')
        #     print('------------------------------')
        
    elif payload["command"] == 'init':

        print('------------------------------')
        print('Init start')

        station_id = int(payload['station'])
        print('Station id is ' + str(station_id))

        post_id = int(payload['post'])
        print('Post id is ' + str(post_id))

        rpi = int(payload['rpi'])
        print('MAC is ' + str(rpi))
        
        station = get_object_or_none(Station, station_id=station_id)
        # station = Station.objects.get(station_id=station_id)
        if station:
            print('Station is ' + station.owner)

            try:
                p = Post.objects.create(
                    post_id = post_id,
                    station = station,
                    mac_uid = rpi
                )
                print('New post is ' + str(p.mac_uid))
                print('------------------------------')
            except:
                print('New post is not created')

client = mqtt.Client()
client.username_pw_set(username="mqttuseruser",password="Uwxd_D41")
client.on_connect = on_connect
client.on_message = on_message

#client.connect("m24.cloudmqtt.com", 13932, 60)
client.connect("192.168.147.14", 1883, 60)
