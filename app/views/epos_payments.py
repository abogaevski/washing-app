import json
from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Post, EposPayment
from app.mqtt.publisher import publish_data

@csrf_exempt
def eposPaymentRequest(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('unicode_escape').encode('latin1').decode('utf8'))

        payment_datetime = datetime.strptime(body["paymentDate"], "%Y-%m-%dT%H:%M:%S.%f")
        post = Post.objects.get(erip_id=body["claimId"])
        amount = body["amount"]["amt"]
        payment_id = body["memorialSlip"]["tranEripId"]
        if post:

            try:
                EposPayment.objects.create( post=post,
                                            pay_date=payment_datetime,
                                            amount=amount,
                                            payment_id=payment_id)
            except:
                print("EposPayment isn't created!")

            course = post.station.course
            points = amount * course
            uid = post.mac_uid

            data = {
                'client': "QR",
                'points': points,
                'payment_id': payment_id
            }
            topic = str(uid) + '/start_washing'
            publish_data(topic, json.dumps(data))
            return HttpResponse('Мойка запускается!{}'.format(data))