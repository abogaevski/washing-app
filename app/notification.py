import requests
from django.core.mail import send_mass_mail
from app.models import User, Post

def sms_notification(msg):

    # http://api.rocketsms.by/simple/send?username=%smsuser%&password=%smspass%&phone=%ph1%&sender=%sender%&text=%msgph%

    URL = "http://ec2-18-223-155-31.us-east-2.compute.amazonaws.com/epos-payment"

    username = "login"
    password = "smspass"
    phone = "phonenum" #check multinum
    sender = "washer"
    #message = msg
    PARAMS = {'username':username, 'password':password, 'phone':phone, 'sender':sender, 'message':msg}
    req = requests.get(url = URL, params = PARAMS)




def email_notification(msg):

    send_mass_mail(
    'Post are unavailable', 
    str(msg),    #'Here is the message.'
    'notify.by.carwash@yandex.ru',
    'notify.by.carwash@yandex.ru',
    )


    # notify.by.carwash@yandex.ru
    # 8y#c4rW45h
