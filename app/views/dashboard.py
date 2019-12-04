from datetime import datetime, timedelta
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from app.models import Contractor, Partner, Payment, UserTransaction, Card, Post
from app.forms import StartWashingForm
from app.mqtt.publisher import publish_data


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        user_transactions_filter_time = datetime.now() - timedelta(days=1)
        partners = Partner.objects.filter(balance__lte=5)
        contractors = Contractor.objects.filter(balance__lte=100)
        posts = Post.objects.filter(is_available=False)
        wash_form = StartWashingForm()
        user_transactions = UserTransaction.objects.filter(date_pub__gte=user_transactions_filter_time)
        payments = Payment.objects.all()

        return render(request,
                      'app/dashboard/dashboard.html',
                      context={
                               'partners': partners,
                               'contractors': contractors,
                               'wash_form': wash_form,
                               'user_transactions': user_transactions,
                               'payments': payments,
                               'posts': posts
                               }
                      )


class StartWash(View):
    def post(self, request):
        bound_form = StartWashingForm(request.POST)

        if bound_form.is_valid():
            uid = bound_form.cleaned_data['post'].mac_uid
            client_uid = ''
            try:
                client_uid = str(bound_form.cleaned_data['card'].data)
            except:
                print('Client not found!')

            course = bound_form.cleaned_data['station'].course
            points = int(bound_form.cleaned_data['payment'] * course)
            if client_uid:
                data = {
                    'client': client_uid,
                    'points': points

                }
            else:
                data = {
                    'client': 'NONE',
                    'points': points
                }

            topic = str(uid) + '/start_washing'
            publish_data(topic, json.dumps(data))
            messages.success(request, 'Мойка запускается!')

            return redirect('/')

        messages.error(request, 'Произошла ошибка! Данные неправильные.')
        return redirect("/")


def load_posts(request):
    if request.is_ajax():
        station_id = request.POST.get('station')
        posts = Post.objects.filter(station_id=station_id).order_by('id')
        return render(request, 'app/dashboard/post_options.html', {'posts': posts})


def load_cards(request):
    if request.is_ajax():
        partner_id = request.POST.get('partner')
        cards = Card.objects.filter(partner_id=partner_id, is_active=True).order_by('id')
        return render(request, 'app/dashboard/cards_options.html', {'cards': cards})
