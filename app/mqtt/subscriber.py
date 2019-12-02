import paho.mqtt.client as mqtt
from .publisher import publish_data
import json
from datetime import datetime
import pytz
from django.conf import settings
from app.utils import get_object_or_none
from django.core.exceptions import ValidationError, FieldError
from decimal import *
import logging

logger = logging.getLogger('mqtt')


def on_connect(client, userdata, flags, rc):
    logger.debug("Connected with result code "+str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    from app.models import Post, Card, Partner, Transaction, Station
    logger.debug('Has a message:' + str(msg.payload))
    payload = json.loads(msg.payload)
    topic = msg.topic.split('/')
    payload['rpi'] = topic[0]
    payload['command'] = topic[1]

    logger.debug('Topic is: ' + msg.topic)

    if payload["command"] == 'account_balance' or payload["command"] == 'start_washing' or payload["command"] == 'srv_ping' or payload["command"] == 'init_reply':
        logger.debug('No action required')

# GET ACCOUNT BALANCE
    elif payload["command"] == 'get_account_balance':

        logger.debug('Get account balance start')

        #- payload["rpi"]
        #- payload["client"]

        rpi = str(payload['rpi'])
        logger.debug('RPI is ' + rpi)
        topic = payload['rpi'] + '/account_balance'
        logger.debug('Topic is ' + topic)

        client = str(payload['client'])
        logger.debug("!!! {} !!!".format(client))
        card = get_object_or_none(Card, data=client)
        logger.debug("!!! {} !!!".format(card.data))

        if card:
            logger.debug('Card is ' + str(card.data))

            client_balance = card.partner.balance
            logger.debug('Balance is ' + str(client_balance))

            post = get_object_or_none(Post, mac_uid=rpi)
            logger.debug(post.mac_uid)
            station = post.station
            logger.debug('Course is ' + str(station.course))
            data = json.dumps({'client': payload["client"], 'balance': float(
                client_balance), 'course': station.course})
            logger.debug(str(data))
        else:
            logger.error('card is not defined')
            data = json.dumps({'client': "NONE"})
            logger.debug(str(data))

        try:
            publish_data(topic, data)
            logger.debug(data)
        except:
            logger.error("Can't send data for account balance")

# TRANSACTIONS
    elif payload["command"] == 'transaction':
        logger.debug('Transaction start')

        # transaction type
        init_type = int(payload['type'])
        logger.debug('Init type is ' + str(init_type))

        # post define
        rpi = str(payload['rpi'])
        logger.debug(rpi)
        post = get_object_or_none(Post, mac_uid=rpi)
        if post:
            logger.debug('Post is ' + str(post.mac_uid))

            # station define
            station = post.station
            logger.debug('Station is ' + station.owner)
            logger.debug(str(post))

            # time define
            timestamp = int(payload['date'])
            start_time_from_timestamp = datetime.fromtimestamp(timestamp)
            tz = pytz.timezone(settings.TIME_ZONE)
            start_time = tz.localize(start_time_from_timestamp)
            logger.debug('Start date is ' + str(start_time))

            # points/price define
            points = int(payload['points'])
            logger.debug('Points is ' + str(points))
            price = points/station.course
            logger.debug('Price is ' + str(price))

            client = str(payload['client'])

            topic = payload['rpi']+'/transaction_reply'
            data = '{"date" : ' + str(payload['date']) + '}'

            try:
                publish_data(topic, data)
                logger.debug(data)
            except:
                logger.error("Can't send data for transaction reply")

            if init_type == 0:

                card = get_object_or_none(Card, data=client)
                if card:
                    logger.debug('Card is ' + str(card))
                    partner = card.partner
                    logger.debug('Partner is ' + partner.name)

                    logger.debug(type(partner.balance))
                    partner.balance -= Decimal(price)
                    logger.debug(
                        'Partner balance after payment is ' + str(partner.balance))

                    try:
                        partner.save()
                    except (ValidationError, FieldError) as err:
                        logger.error('Partner is not save ' + str(err))

                    try:
                        t = Transaction.objects.create(
                            card=card,
                            partner=partner,
                            station=station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                        logger.debug(t)
                    except:
                        logger.error(
                            'Transaction with partner and card not created')

            elif init_type == 1:

                if client == "NONE":

                    try:
                        t = Transaction.objects.create(
                            station=station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                        logger.debug(t)
                    except:
                        logger.error('Transaction not created')

                elif client:
                    card = get_object_or_none(Card, data=client)
                    if card:
                        logger.debug('Card is ' + str(card))
                        partner = card.partner
                        logger.debug('Partner is ' + partner.name)

                        logger.debug(type(partner.balance))
                        partner.balance -= Decimal(price)
                        logger.debug(
                            'Partner balance after payment is ' + str(partner.balance))

                    try:
                        partner.save()
                    except (ValidationError, FieldError) as err:
                        logger.error('Partner is not save ' + str(err))

                    try:
                        t = Transaction.objects.create(
                            card=card,
                            partner=partner,
                            station=station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                        logger.debug(t)
                    except:
                        logger.error(
                            'Transaction with partner and card not created')
                else:
                    logger.error(
                        'Undefined client. Not created')

            elif init_type == 2:
                try:
                    t = Transaction.objects.create(
                        station=station,
                        post=post,
                        start_time=start_time,
                        price=price,
                        initiator_type=init_type
                    )
                    logger.debug(t)
                except:
                    logger.error('Transaction not created')

            else:
                logger.error('Undefined transaction type. Not created')
        else:
            logger.error('Undefined post. Not created')


# INITIALIZATION
    elif payload["command"] == 'init':

        logger.debug('Init start')

        station_id = int(payload['station'])
        logger.debug('Station id is ' + str(station_id))

        post_id = int(payload['post'])
        logger.debug('Post id is ' + str(post_id))

        rpi = str(payload['rpi'])
        logger.debug('MAC is ' + str(rpi))

        station = get_object_or_none(Station, station_id=station_id)
        logger.debug('Station is ' + str(station))

        # is station+post+mac exist
        if not get_object_or_none(Post, station=station, post_id=post_id, mac_uid=rpi):
            # is station+post exist
            if not get_object_or_none(Post, station=station, post_id=post_id):
                # is device exist
                if not get_object_or_none(Post, mac_uid=rpi):  

                    try:
                        p = Post.objects.create(
                            post_id=post_id,
                            station=station,
                            mac_uid=rpi
                        )
                        logger.debug('New post is ' + str(p.mac_uid))
                        status = "initOK"
                    except:
                        logger.error('New post is not created')
                        status = "error"

                else:
                    data = "devExist"
                    logger.error('Device ' + str(rpi) +
                                 ' already exist on other post/station')

            else:
                status = "postDuplicate"
                logger.error('Another device is set to station ' + str(station_id) + ' post ' + str(post_id))


        else:
            status = "postExist"
            logger.debug('Post already exist')

        topic = payload['rpi'] + '/init_reply'
        data = json.dumps({'status': status})
        try:
            publish_data(topic, data)
            logger.debug('Sent data' + data)
        except:
            logger.error("Can't send init reply data")

# PING
    elif payload["command"] == 'rpi_ping':
        rpi = str(payload['rpi'])
        timestamp = int(payload['date'])
        start_time_from_timestamp = datetime.fromtimestamp(timestamp)
        tz = pytz.timezone(settings.TIME_ZONE)
        last_seen = tz.localize(start_time_from_timestamp)
        post = get_object_or_none(Post, mac_uid=rpi)
        if post:
            logger.debug("Post is {}".format(post.station.owner))
            post.last_seen = last_seen
            try:
                partner.save()
            except (ValidationError, FieldError) as err:
                logger.error('Post is not save ' + str(err))

        logger.debug('Rpi ' + rpi + ' is available!')


client = mqtt.Client()
client.username_pw_set(username="mqttuser", password="Uwxd_D41")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
