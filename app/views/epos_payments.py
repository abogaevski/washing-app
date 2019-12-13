import json
from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Post, EposPayment

@csrf_exempt
def eposPaymentRequest(request):
    if request.method == "POST":
        body = json.loads(request.body)
        payment_datetime = datetime.strptime(body["paymentDate"], "%Y-%m-%dT%H:%M:%S.%f")
        post = Post.objects.get(erip_id=body["claimId"])
        amount = body["amount"]["amt"]
        if post:

            try:
                EposPayment.objects.create( post=post,
                                            pay_date=payment_datetime,
                                            amount=amount)
            except:
                print("EposPayment isn't created!")

            course = post.station.course
            points = amount * course
            uid = post.mac_uid

            data = {
                'client': 'QR',
                'points': points
            }
            topic = str(uid) + '/start_washing'
            # publish_data(topic, json.dumps(data))
            return HttpResponse('Мойка запускается!{}'.format(data))