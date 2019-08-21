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
import logging

logger = logging.getLogger('mqtt')

def on_connect(client, userdata, flags, rc):
    logger.debug("Connected with result code "+str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    from app.models import Post, Card, Partner, Transaction, Station
    logger.debug('Has a message:' + str(msg.payload))
    payload=json.loads(msg.payload)
    topic=msg.topic.split('/')
    payload['rpi'] = topic[0]
    payload['command'] = topic[1]

    # logger.debug('Payload is: ' + str(payload))
    logger.debug('Topic is: ' + msg.topic)


    if payload["command"] == 'account_balance' or payload["command"] == 'start_washing' or payload["command"] == 'srv_ping':
        logger.debug('No action required')


    elif payload["command"] == 'get_account_balance':

        logger.debug('Get account balance start')

        
        #- payload["rpi"]
        #- payload["client"]
        client = str(payload['client'])
        # card = Card.objects.get(data=client)
        card = get_object_or_none(Card, data=client)
        
        if card:
            logger.debug('Card is ' + str(card.data))
            
            client_balance = card.partner.balance
            logger.debug('Balance is ' + str(client_balance))

            #**************************
            #*******xdsi***************
            rpi=str(payload['rpi'])
            logger.debug('RPI is ' + rpi)
            post = get_object_or_none(Post, mac_uid=rpi)
            logger.debug(post.mac_uid)
            station=post.station
            logger.debug('Course is ' + str(station.course))
            #- fuction check balance and send it
            topic = payload['rpi'] + '/account_balance'
            logger.debug('Topic is ' + topic)

            #**************************
            #*******xdsi***************
            data = json.dumps({'client': payload["client"], 'balance': float(client_balance), 'course': station.course})
            logger.debug( str(data) )
            try:
                publish_data(topic, data)
                logger.debug( data )
            except:
                logger.debug("Can't send data for account balance")        
        else:
            logger.debug('card is not defined')
    

    # TRANSACTIONS
    elif payload["command"] == 'transaction':
        logger.debug('Transaction start')

        init_type = int(payload['type'])
        logger.debug('Init type is ' + str(init_type))

        rpi = str(payload['rpi'])
        # post = Post.objects.get(mac_uid=rpi)
        post = get_object_or_none(Post, mac_uid=rpi)
        if post:
            logger.debug('Post is ' + str(post.mac_uid))
            station = post.station
            logger.debug('Station is ' + station.owner)       

        timestamp = int(payload['date'])
        start_time_from_timestamp = datetime.fromtimestamp(timestamp)
        tz = pytz.timezone(settings.TIME_ZONE)
        start_time = tz.localize(start_time_from_timestamp)

        logger.debug('Start date is ' + str(start_time))


#**************************
#*******xdsi***************
        points = int(payload['points'])
        logger.debug('Points is ' + str(points))
        station = post.station
        price = points/station.course
        logger.debug('Price is ' + str(price))
        logger.debug(type(price))


        if init_type != 2:
            
            client = str(payload['client'])

            card = get_object_or_none(Card, data=client)
            if card:
                logger.debug('Card is ' + str(card))
                partner = card.partner
                logger.debug('Partner is ' + partner.name)     

            logger.debug(type(partner.balance))
            partner.balance -= Decimal(price)
            logger.debug('Partner balance after payment is ' + str(partner.balance))

            try:
                partner.save()
            except (ValidationError, FieldError) as err:
                logger.debug('Partner is not save ' + str(err))

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
                logger.debug(t)
            except:
                logger.debug('Transaction with partner and card not created')

        try:
            t = Transaction.objects.create(
                station = station,
                post = post,
                start_time = start_time,
                price = price,
                initiator_type = init_type
            )
            logger.debug(t)
        except:
            logger.debug('Transaction not created')
                
        
    elif payload["command"] == 'init':

        logger.debug('Init start')

        station_id = int(payload['station'])
        logger.debug('Station id is ' + str(station_id))

        post_id = int(payload['post'])
        logger.debug('Post id is ' + str(post_id))

        rpi = int(payload['rpi'])
        logger.debug('MAC is ' + str(rpi))
        
        station = get_object_or_none(Station, station_id=station_id)
        if station:
            logger.debug('Station is ' + station.owner)

            try:
                p = Post.objects.create(
                    post_id = post_id,
                    station = station,
                    mac_uid = rpi
                )
                logger.debug('New post is ' + str(p.mac_uid))
            except:
                logger.debug('New post is not created')

    elif payload["command"] == 'rpi_ping':
        rpi = payload['rpi']
        logger.debug('Rpi ' + rpi + 'is available')

# client = mqtt.Client()
client = mqtt.Client()
client.username_pw_set(username="mqttuseruser",password="Uwxd_D41")
client.on_connect = on_connect
client.on_message = on_message

#client.connect("m24.cloudmqtt.com", 13932, 60)
client.connect("192.168.147.14", 1883, 60)
