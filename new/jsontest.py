import json
import time

#payload=json.loads(msg.payload.decode("utf-8"))
#topic=msg.topic.split('/')

# payload={"client":0x0A1B2C3D4E5F60,"payment":1}
# topic=["0A1B2C3D4E5F", "start_washing"]

payload={"client":0x0A1B2C3D4E5F60}
topic=["0A1B2C3D4E5F", "get_account_balance"]

payload["rpi"]=topic[0]
payload["command"]=topic[1]


if payload["command"] == 'account_balance' or payload["command"] == 'start_washing' or payload["command"] == 'srv_ping':
    print("no action")
elif payload["command"] == 'get_account_balance':
    #- payload["rpi"]
    #- payload["client"]
    
    #- fuction check balance and send it
    
    #- check balance function returns int client_balance
    #client_balance=check_balance(payload["client"])

    #publish_data(topic,json.dumps({'client': payload["client"], 'balance': client_balance}))
    print(json.dumps({'client': payload["client"], 'balance': 7}))

elif payload["command"] == 'transaction':
    #- payload["rpi"]
    #- payload["client"]
    #- payload["payment"]
    #- payload["date"]
    #- payload["type"]

    #- function write transaction to DB
    from app.models import Transaction

    #partner = select_partner_from_DB(payload["client"])
    #station = select_station_from_DB(payload["rpi"])
    #post = select_post_from_DB(payload["rpi"])

    # Transaction.objects.create(
    #     card = payload["client"],
    #     partner = partner,
    #     station = station,
    #     post = post,
    #     start_time = payload["date"],
    #     price = payload["payment"],
    #     initiator_type = payload["type"],
    # )

    print("transaction")

elif payload["command"] == 'init':
    #- payload["rpi"]
    #- payload["station"]
    #- payload["post"]

    # function write new post to DB

    print("init")

elif payload["command"] == 'rpi_ping':
    #- payload["rpi"]
    
    #- invent function set post available

    print("ping")

else :
    print("err topic")