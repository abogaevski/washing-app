import os
import sys
import json
import pytz
import logging

from datetime import datetime
from decimal import *

from django.conf import settings
from django.core.exceptions import ValidationError, FieldError

import paho.mqtt.client as mqtt

from app.utils import get_object_or_none


logger = logging.getLogger('mqtt')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    from app.models import Post, Card, Partner, Transaction, Station, EposPayment
    print("-----------------------------------")

    print("DEBUG: Has a message. {}".format(msg.payload))
    try:
        payload = json.loads(msg.payload)
        print("DEBUG: Payload is loaded to JSON {}".format(payload))
    except ValueError as error:
        print("ERROR: JSON payload isn't loads. Exit with error. {}".format(error))
        return False

    print('DEBUG: Topic is: {}'.format(msg.topic))

    topic = msg.topic.split("/")
    payload["rpi"] = topic[0]
    payload["command"] = topic[1]

    print("-----------------------------------")
    
    # ACCOUNT BALANCE, START WASHING, SRV PING, INIT REPLY
    if payload["command"] == 'account_balance' or payload["command"] == 'start_washing' or payload["command"] == 'srv_ping' or payload["command"] == 'init_reply':
        print('No action required')
        return True

    # GET ACCOUNT BALANCE
    elif payload["command"] == 'get_account_balance':

        print("DEBUG: Get account balance start...")

        rpi = str(payload['rpi'])
        print("DEBUG: RPI is: {}".format(rpi))

        topic = payload['rpi'] + '/account_balance'
        print("DEBUG: Topic to reply is: {}".format(topic))

        client_data = str(payload['client'])
        print("DEBUG: Client data is: {}".format(client_data))

        print("DEBUG: Getting card object from client_data...")
        card = get_object_or_none(Card, data=client_data)
        print("DEBUG: Card is: {}".format(card))

        if card:
            print("DEBUG: Card is defined. Continue...")

            client_balance = card.partner.balance
            print("DEBUG: Client balance is {}".format(client_balance))

            print("DEBUG: Getting post object from rpi...")
            post = get_object_or_none(Post, mac_uid=rpi)
            print("DEBUG: Post is: {}".format(post))

            if post:
                print("DEBUG: Getting station object from post {}...".format(post))
                station = post.station
                print("DEBUG: Station is: {}".format(station))

                print("DEBUG: Getting station course in station {}...".format(station))
                station_course = station.course
                print('DEBUG: Station course is {}'.format(station_course))
            else:
                print("DEBUG: Post isn't defined. Exit.")
                return False

            print('DEBUG: Trying collect data...')
            try:
                data = json.dumps({ 'client': payload["client"],
                                    'balance': float(client_balance),
                                    'course': station_course
                                })
            except ValueError as error:
                print("ERROR: JSON data isn't dumps. Exit with error. {}".format(error))
                return False
            print('DEBUG: Data is {}'.format(data))    

        else:
            print("DEBUG: Card isn't defined. Collecting data and sending that client: none")
            data = json.dumps({'client': "NONE"})
            print("DEBUG: Data is {}".format(data))

        try:
            print("DEBUG: Trying to send data...")
            client.publish(topic, payload=str(data), retain=False)
        except:
            print("ERROR: Can't send data for account balance")
            return False
        
        print("DEBUG: Data {} has already sent to topic {}".format(data, topic))
        return True
    
    # TRANSACTION
    elif payload["command"] == 'transaction':
        
        print("DEBUG: Transation start...")

        rpi = str(payload['rpi'])
        print("DEBUG: RPI is: {}".format(rpi))

        print("DEBUG: Getting post object from rpi...")
        post = get_object_or_none(Post, mac_uid=rpi)
        print("DEBUG: Post is: {}".format(post))

        if post:
            
            print("DEBUG: Defining transaction start time...")
            timestamp = int(payload['date'])
            start_time = pytz.timezone(settings.TIME_ZONE).localize(datetime.fromtimestamp(timestamp))
            print("DEBUG: Start time: {}".format(start_time))

            points = int(payload['points'])
            print("DEBUG: Points: {}".format(points))

            station_course = post.station.course
            print("DEBUG: Station course: {}".format(station_course))
            
            price = points / station_course
            print("DEBUG: Price: {}".format(price))

            init_type = int(payload['type'])
            print("DEBUG: Init type: {}".format(init_type))

            client_data = str(payload['client'])
            print("DEBUG: Client data is: {}".format(client_data))

            print("DEBUG: Collecting data for transaction reply...")

            topic = rpi + '/transaction_reply'
            print("DEBUG: Topic: {}".format(topic))
            #TODO: Correct it!
            # data = '{"date" : {}}'.format(timestamp)
            # print("DEBUG: Data: {}".format(data))


            try:
                print("DEBUG: Trying to send transaction reply...")
                client.publish(topic, payload=data, retain=False)
                
            except:
                print("ERROR: Can't send transaction reply")
            
            if init_type == 0:

                print("DEBUG: Initiator type: 0 (Controller)")

                print("DEBUG: Getting card object from client data...")
                card = get_object_or_none(Card, data=client_data)
                print("DEBUG: Card is: {}".format(card))

                if card:
                    partner = card.partner
                    print('DEBUG: Partner: {}'.format(partner))

                    partner.balance -= Decimal(price)
                    print("DEBUG: Partner balance after payment: {}".format(partner.balance))

                    try:
                        print("DEBUG: Trying save partner...")
                        partner.save()
                    except (ValidationError, FieldError) as err:
                        print("ERROR: Partner isn't save. Exit.")
                        return False
                    finally:
                        print("DEBUG: Partner saved...")
                    
                    try:
                        print("DEBUG: Trying create transaction...")
                        transaction = Transaction.objects.create(
                            card=card,
                            partner=partner,
                            station=post.station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                    except:
                        print("ERROR: Transaction not created. Error: {}".format(sys.exc_info()))
                        return False
                    finally:
                        print("DEBUG: Transaction created: {}".format(transaction))
                        return True
                    
                else: 
                    print("ERROR: Card with data {} isn't defined".format(client_data))
                    return False
            
            elif init_type == 1:
                
                print("DEBUG: Initiator type: 1 (Web Application)")
                print("DEBUG: Client data:".format(client_data))

                print("DEBUG: Getting card object from client data...")
                card = get_object_or_none(Card, data=client_data)
                print("DEBUG: Card is: {}".format(card))

                if card:
                    partner = card.partner
                    print('DEBUG: Partner: {}'.format(partner))

                    partner.balance -= Decimal(price)
                    print("DEBUG: Partner balance after payment: {}".format(partner.balance))

                    try:
                        print("DEBUG: Trying save partner...")
                        partner.save()
                    except (ValidationError, FieldError) as err:
                        print("ERROR: Partner isn't save. Exit.")
                        return False
                    finally:
                        print("DEBUG: Partner saved...")
                    
                    try:
                        print("DEBUG: Trying create transaction...")
                        transaction = Transaction.objects.create(
                            card=card,
                            partner=partner,
                            station=post.station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                    except:
                        print("ERROR: Transaction not created. Error: {}".format(sys.exc_info()))
                        return False
                    finally:
                        print("DEBUG: Transaction created: {}".format(transaction))
                        return True
                    
                elif client_data == "NONE":
                    try:
                        print("DEBUG: Trying create transaction...")
                        transaction = Transaction.objects.create(
                            station=post.station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                    except:
                        print("ERROR: Transaction not created. Error: {}".format(sys.exc_info()))
                        return False
                    finally:
                        print("DEBUG: Transaction created: {}".format(transaction))
                        return True
                else:
                    print("ERROR: Wrong client data for this init type. Client data: {}".format(client_data))
                    return False

            elif init_type == 2:
                print("DEBUG: Initiator type: 2 (Money)")
                try:
                    print("DEBUG: Trying create transaction...")                   
                    transaction = Transaction.objects.create(
                        station=post.station,
                        post=post,
                        start_time=start_time,
                        price=price,
                        initiator_type=init_type
                    )
                except:
                    print("ERROR: Transaction not created. Error: {}".format(sys.exc_info()))
                    return False
                finally:
                    print("DEBUG: Transaction created: {}".format(transaction))
                    return True
            
            elif init_type == 3:
                print("DEBUG: Initiator type: 3 (EPOS Payment)")

                if client_data == "QR": 
                    try:
                        print("DEBUG: Trying create transaction...")
                        transaction = Transaction.objects.create(
                            station=post.station,
                            post=post,
                            start_time=start_time,
                            price=price,
                            initiator_type=init_type
                        )
                    except:
                        print("ERROR: Transaction not created. Error: {}".format(sys.exc_info()))
                        return False
                    finally:
                        print("DEBUG: Transaction created: {}".format(transaction))

                    if transaction:

                        payment_id = str(payload['payment_id'])
                        print("DEBUG: Payment id: {}".format(payment_id))

                        print("DEBUG: Getting payment from: {}".format(payment_id))
                        payment = get_object_or_none(EposPayment, is_passed=False, payment_id=payment_id)
                        
                        if payment:
                            payment.is_passed = True
                            print("DEBUG: Change payment to passed status.")

                            try:
                                print("DEBUG: Trying save payment...")
                                payment.save()
                            except (FieldError, ValidationError) as error:
                                print("ERROR: Payment isn't save. {}".format(error))
                                return False
                            
                            print("DEBUG: Payment {} saved.".format(payment))
                            return True
                        else:
                            print("ERROR: No payment for transaction {}. Payment id: {}".format(transaction, payment_id))
                            return False

                # If client QR
                else:
                    print("ERROR: Client not like QR. Client data: {}".format(client_data))
                    return False
            
            #if init type
            else:
                print("ERROR: Undefined initiator type. Init type: {}".format(init_type))
                return False
        
        # if post
        else:
            print("ERROR: Undefined post. RPI: {}".format(rpi))
            return False

    # INIT
    elif payload["command"] == 'init':
        
        print("DEBUG: Post initialization starting...")
        
        station_id = int(payload['station'])
        print("DEBUG: Station id: {}".format(station_id))

        station = get_object_or_none(Station, station_id=station_id)
        print("DEBUG: Station: {}".format(station))

        post_id = int(payload['post'])
        print("DEBUG: Post id:".format(post_id))

        rpi = str(payload['rpi'])
        print("DEBUG: RPI: {}".format(rpi))

        # is station+post+mac exist
        print("DEBUG: Start checking existing the post.")
        if not get_object_or_none(Post, station=station, post_id=post_id, mac_uid=rpi):
            
            print("DEBUG: Post with this station: {}, post id: {}, rpi: {} not exist".format(station, post_id, rpi))
            # is station+post exist
            if not get_object_or_none(Post, station=station, post_id=post_id):
            
                print("DEBUG: Post with this station: {}, post id: {} not exist".format(station, post_id))
                # is device exist
                if not get_object_or_none(Post, mac_uid=rpi):
            
                    print("DEBUG: Post with this rpi: {} not exist. Creating...".format(rpi))
                    try:
                        
                        print("DEBUG: Trying create post...")
                        post = Post.objects.create(
                            post_id=post_id,
                            station=station,
                            mac_uid=rpi
                        )

                        status = "initOK"
                        print("DEBUG: Changed status to initOK.")

                    except:

                        print("ERROR: Post isn't created.")

                        status = "error"
                        print("ERROR: Changed status to error.")
                
                # If rpi exists
                else:

                    status = "devExist"
                    print("WARNING: Device is already exist. Changed status to devExist.")

            #if station + post exist
            else:

                status = "postDuplicate"
                exist_post = get_object_or_none(Post, station=station, post_id=post_id)
                print("WARNING: Another device is already exist here. Post: {}".format(exist_post))

        # if station + post + rpi exist
        else:
            
            status = "postExist"
            print("WARNING: Post is already exist here.")

        topic = "{}/init_reply".format(rpi)

        try:
            print("DEBUG: Trying collecting data for reply. Status: {}".format(status))
            data = json.dumps({"status": status})
        except ValueError as error:
            print("ERROR: JSON status isn't loads. Exit with error. {}".format(error))
            return False
        
        try:
            print("DEBUG: Trying send status to...")
            client.publish(topic, payload=str(data), retain=False)
        except:
            print("ERROR: Status {} isn't send".format(status))
            return False
        finally:
            print("DEBUG: Status {} has already sent".format(status))
    
    # PING
    elif payload["command"] == 'rpi_ping':
        
        print("DEBUG: Post ping start...")

        rpi = str(payload['rpi'])
        print("DEBUG: RPI is: {}".format(rpi))

        print("DEBUG: Getting post object from rpi...")
        post = get_object_or_none(Post, mac_uid=rpi)
        print("DEBUG: Post is: {}".format(post))

        print("DEBUG: Defining post last seen time...")
        timestamp = int(payload['date'])
        last_seen = pytz.timezone(settings.TIME_ZONE).localize(datetime.fromtimestamp(timestamp))
        print("DEBUG: Last seen: {}".format(last_seen))

        if post:

            print("DEBUG: Changing post last seen time and set as available...")
            post.last_seen = last_seen
            post.is_available = True

            try:
                
                print("DEBUG: Trying save post {}".format(post))
                post.save()
            except (ValidationError, FieldError) as error:
                
                print("ERROR: Post isn't save. Error: {}".format(error))
                return False
            finally:
                
                print("DEBUG: Post has been changed and saved.")
                return True
        else:
            print("ERROR: Undefined post. RPI: {}".format(rpi))



def main():
    client = mqtt.Client()
    client.username_pw_set(username="mqttuser", password="Uwxd_D41")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_forever()


# if __name__ == "__main__": 
#     main()







# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine.settings_prod")

# print(os)

# import paho.mqtt.client as mqtt
# from app.publisher import publish_data
# import json
# from datetime import datetime
# import pytz
# from django.conf import settings
# from app.utils import get_object_or_none
# from django.core.exceptions import ValidationError, FieldError
# from decimal import *
# import logging