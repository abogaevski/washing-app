from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.generic import View
from .models import *
from .forms import *
from .mqtt.publisher import publish_data
from .utils import *
import json
import time 
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from django.forms.models import model_to_dict
from django.db.models import  Q
import re

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape


# Create your views here.
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        last_day = datetime.now() - timedelta(hours = 24)

        tz = pytz.timezone(settings.TIME_ZONE)
        last_day = tz.localize(last_day)

        transactions = Transaction.objects.filter(start_time__gte=last_day)
        partners = Partner.objects.filter(balance__lte=5)
        contractors = Contractor.objects.filter(balance__lte=5)
        wash_form = StartWashingForm()

        # post_transactions_sum = Transaction.objects.all().aggregate(Sum('price'))


        user_transactions = UserTransaction.objects.filter(date_pub__gte=last_day)

        return render(  request,
                        'app/dashboard/dashboard.html',
                        context= {  'transactions': transactions,
                                    'partners': partners,
                                    'contractors': contractors,
                                    'wash_form': wash_form,
                                    'user_transactions': user_transactions
                                    }
                    )


class StartWash(View):
    def post(self, request):
        bound_form = StartWashingForm(request.POST['data'])

        if bound_form.is_valid():
            uid = bound_form.cleaned_data['post'].mac_uid
            client_uid = ''
            try:
                client_uid = str(bound_form.cleaned_data['card'].data)
                print(client_uid)
            except:
                print('Client not found!')

            course = bound_form.cleaned_data['station'].course
            # points = bound_form.cleaned_data['payment'] * course
            # points = ( bound_form.cleaned_data['payment'] * course )  // 1
            points = int( bound_form.cleaned_data['payment'] * course )
            if client_uid:
                data = {
                    # Change!
                    'client': client_uid,
                    'points': points

                }
            else:
                data = {
                    'points': points
                }

            topic = str(uid) + '/start_washing'
            publish_data(topic, json.dumps(data))
            messages.success(request, 'Мойка запускается!')

            return redirect('/')

        messages.error(request, 'Произошла ошибка!')
        return redirect("/")

def load_posts(request):
    if request.is_ajax():
        station_id = request.POST.get('station')
        posts = Post.objects.filter(station_id=station_id).order_by('id')
        return render(request, 'app/dashboard/post_options.html', {'posts': posts})


def load_cards(request):
    if request.is_ajax():
        partner_id = request.POST.get('partner')
        cards = Card.objects.filter(partner_id=partner_id).order_by('id')
        return render(request, 'app/dashboard/cards_options.html', {'cards': cards})

# ----------------------------------------------
# Entity lists
# ObjectListMixin in utils.py
# ----------------------------------------------

class TransactionList(LoginRequiredMixin, ObjectListMixin, View):
    model = Transaction
    template = 'app/transaction/transaction_list.html'
    context = 'transactions'  


class PartnerList(LoginRequiredMixin, ObjectListMixin, View):
    model = Partner
    template = 'app/partner/partner_list.html'
    context = 'partners'


class ContractorList(LoginRequiredMixin, ObjectListMixin, View):
    model = Contractor
    template = 'app/contractor/contractor_list.html'
    context = 'contractors'


class CardList(LoginRequiredMixin, ObjectListMixin, View):
    model = Card
    template = 'app/card/card_list.html'
    context = 'cards'
        

class StationList(LoginRequiredMixin, ObjectListMixin, View):
    model = Station
    template = 'app/station/station_list.html'
    context = 'stations'


class PostList(LoginRequiredMixin, ObjectListMixin, View):
    model = Post
    template = 'app/post/post_list.html'
    context = 'posts'


class PaymentList(LoginRequiredMixin, ObjectListMixin, View):
    model = Payment
    template = 'app/payment/payment_list.html'
    context = 'payments'


class UserTransactionList(LoginRequiredMixin, ObjectListMixin, View):
    model = UserTransaction
    template = 'app/user_transaction/user_transaction_list.html'
    context = 'transactions'

# ----------------------------------------------
# End entity lists
# ----------------------------------------------


# ----------------------------------------------
# Get deatils functions
# objectDetailRequest function in utils.py
# ----------------------------------------------

def partnerDetailRequest(request):
    model = Partner
    template = 'app/partner/partner_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))

def contractorDetailRequest(request):
    model = Contractor
    template = 'app/contractor/contractor_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))

def cardDetailRequest(request):
    model = Card
    template = 'app/card/card_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))

def stationDetailRequest(request):
    model = Station
    template = 'app/station/station_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))


# ----------------------------------------------
# End get deatils functions
# ----------------------------------------------


# ----------------------------------------------
# Create object functions
# ObjectCreateMixin in utils.py
# ----------------------------------------------

class PartnerCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = PartnerForm
    template = 'app/partner/partner_create.html'


class ContractorCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = ContractorForm
    template = 'app/contractor/contractor_create.html'


class StationCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = StationForm
    template = 'app/station/station_create.html'


class CardCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = CardForm
    template = 'app/card/card_create.html'


class CardActive(LoginRequiredMixin, View):
    def get(self, request):
        form = CardForm
        return render(request, 'app/card/card_create.html', context={'form': form})

    def post(self, request):
        bound_form = CardForm(request.POST['data'])
        if bound_form.is_valid():
            bound_obj = ''
            try:
                bound_obj = Card.objects.get(data=bound_form.cleaned_data['data'])
            except: 
                new_obj = bound_form.save()
                messages.success(request, 'Вы cоздали ' + str(new_obj))

            if bound_obj:
                if not bound_obj.is_active:
                    bound_obj.partner = bound_form.cleaned_data['partner']
                    bound_obj.is_active = True
                    bound_obj.save()
                    messages.success(request, 'Вы включили {0} '.format(bound_obj))
                else:
                    messages.warning(request,   'Вы не можете включить {0}. Уже включена '
                                                .format(bound_obj))      

        return redirect('/')


class PaymentCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = PaymentForm
        return render(request, 'app/payment/payment_create.html', context={'form': form})
    def post(self, request):
        message = 'Добавление платежа. '
        bound_form = PaymentForm(request.POST)
        # print(str(bound_form))
        if bound_form.is_valid():
            contractor = bound_form.cleaned_data['contractor']
            amount = bound_form.cleaned_data['amount']

            if contractor:
                contractor.balance += amount
                contractor.save()
                print('Contractor balance is ' + str(contractor.balance))

            new_obj = bound_form.save()

            message += 'Успешно. Платеж для "'+ contractor.name +'" добавлен с примечанием: "' + bound_form.cleaned_data['annotation'] + '"'
            messages.success(request, message)
            
            UserTransaction.objects.create(
                    entity='Контрагент: ' + contractor.name,
                    user=request.user,
                    annotation=message,
                    exec_type=1,
                    amount= amount
                )

            return redirect('payment_list_url')

        message += 'Ошибка. Платеж для "'+ contractor.name +'" не добавлен с примечанием: "' + bound_form.cleaned_data['annotation'] + '"'
        messages.error(request, message)

        UserTransaction.objects.create(
            entity='Контрагент: ' + contractor.name,
            user=request.user,
            annotation=message,
            exec_type=0,
            amount= amount
        )

        return redirect('payment_list_url')
    
        # return HttpResponseRedirect(reverse('jobs'))

# ----------------------------------------------
# End create object functions
# ----------------------------------------------


# ----------------------------------------------
# Update object functions
# ObjectUpdateMixin in utils.py
# ----------------------------------------------

class PartnerUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Partner
    model_form = PartnerForm
    template = 'app/partner/partner_update.html'


class ContractorUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Contractor
    model_form = ContractorForm
    template = 'app/contractor/contractor_update.html'


class StationUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Station
    model_form = StationForm
    template = 'app/station/station_update.html'

class CardUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Card
    model_form = CardForm
    template = 'app/card/card_update.html'


class PartnerAddCoins(LoginRequiredMixin, View):
    def get(self, request, id):
        partner = Partner.objects.get(id=id)
        bound_form = PartnerCoinForm(instance=partner)

        return render ( request, 'app/partner/partner_add_coins.html',
                        context={   'form': bound_form,
                                    'partner': partner})

    def post(self, request, id):
        partner = Partner.objects.get(id=id)
        bound_form = PartnerCoinForm(request.POST['data'], instance=partner)
        partner_balance = partner.balance

        if bound_form.is_valid():
            contractor_balance = partner.contractor.balance
            partner_balance_in_form = bound_form.cleaned_data['balance']
            message = 'Изменение баланса клиента. '

            if partner_balance_in_form > contractor_balance:
                message +=   'Ошибка. Вы указали баланс больше, чем имеется у контрагента.\
                            Пожалуйста, добавьте баланс контрагенту перед тем как добавить Клиенту!'
                messages.error(request, message)

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=0,
                    amount=partner_balance_in_form
                )

                return redirect('partner_list_url')

            elif (partner_balance + partner_balance_in_form) < 0:
                message += 'Ошибка. У партнера не может быть меньше нуля'
                messages.warning(request, message)

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=0,
                    amount=partner_balance_in_form
                )
                return redirect('partner_list_url')


            else: 
                contractor = partner.contractor
                new_contractor_balance = contractor_balance - partner_balance_in_form
                contractor.balance = new_contractor_balance
                contractor.save()
                
                new_partner_balance = partner_balance + partner_balance_in_form
                new_partner_obj = bound_form.save(commit=False)
                new_partner_obj.balance = new_partner_balance
                new_partner_obj.save()

                message += 'Успешно. Добавлено ' + str(partner_balance_in_form) + ' к ' + new_partner_obj.name

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=1,
                    amount=partner_balance_in_form
                )

                messages.success(request, message)
                return redirect('partner_list_url')
            
        
        message += 'Ошибка. Произошла ошибка добавления!'
        messages.error(request, message)
        return redirect('partner_list_url')


def partnerAddCoinsRequest(request):
    if request.is_ajax():
        post = request.POST['data']
        
        partner = Partner.objects.get(id=post['item'])
        partner_balance = partner.balance

        bound_form = PartnerCoinForm(request.POST['data'], instance=partner)
        message = "Изменение баланса клиента. "

        if bound_form.is_valid():
            contractor_balance = partner.contractor.balance
            partner_balance_in_form = bound_form.cleaned_data['balance']

            # return JsonResponse({"partner": contractor_balance})

            if partner_balance_in_form > contractor_balance:
                message += "Ошибка! Вы добавили больше, чем имеется у контрагента"

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=0,
                    amount=partner_balance_in_form
                )

                return JsonResponse({"message": message, "class": "alert-warning", 'partner': partner.id })         

            elif (partner_balance + partner_balance_in_form) < 0:

                message += "Ошибка. У партнера не может быть меньше нуля"
                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=0,
                    amount=partner_balance_in_form
                )
                return JsonResponse({"message": message, "class": "alert-warning", 'partner': partner.id })

            else: 
                contractor = partner.contractor
                new_contractor_balance = contractor_balance - partner_balance_in_form
                contractor.balance = new_contractor_balance
                contractor.save()
                
                new_partner_balance = partner_balance + partner_balance_in_form
                new_partner_obj = bound_form.save(commit=False)
                new_partner_obj.balance = new_partner_balance
                new_partner_obj.save()

                message += 'Успешно. Добавлено ' + str(partner_balance_in_form) + ' к ' + new_partner_obj.name

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=1,
                    amount=partner_balance_in_form
                )

                return JsonResponse({"message": message, "class": "alert-success", 'new_balance': new_partner_balance, 'new_contractor_balance': new_contractor_balance,'partner': partner.id })
        message += "Произошла ошибка!"
        
        UserTransaction.objects.create(
            entity='Клиент: ' + partner.name,
            user=request.user,
            annotation=message,
            exec_type=1,
            amount=partner_balance_in_form
        )
        return JsonResponse({"message": message + str(bound_form.errors), "class": "alert-danger", 'partner': partner.id })

            
            

        # return redirect('/')


class ContractorDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Contractor
    template = 'app/contractor/contractor_delete.html'


class PartnerDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Partner
    template = 'app/partner/partner_delete.html'


# class StationDelete(LoginRequiredMixin, OjectDisableMixin, View):
#     model = Station
#     template = 'app/station/station_delete.html'


class CardDelete(LoginRequiredMixin, OjectDisableMixin, View):
    model = Card
    template = 'app/card/card_delete.html'


class TransactionListJson(LoginRequiredMixin, BaseDatatableView):
    model = Transaction
    columns = ['id', 'card', 'partner', 'station', 'post', 'start_time', 'price']
    order_columns = ['id', 'card', 'partner', 'station', '', 'start_time', '']

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        tz = pytz.timezone(settings.TIME_ZONE)

        for item in qs:
            if item.card:
                new_card = item.card.data
            else: 
                new_card = "Нет карты"

            if item.partner:
               new_partner = item.partner.name
            else:
                new_partner = "Нет партнера"

            if item.start_time:
                item.start_time = tz.normalize(item.start_time)

            json_data.append([
                escape(item.id),  # escape HTML for security reasons
                escape("{0}".format(new_card)),  
                escape("{0}".format(new_partner)), 
                escape("{0}".format(item.station.owner)),  # escape HTML for security reasons
                escape("{0}".format(item.post.id)),  # escape HTML for security reasons
                item.start_time.strftime("%d.%m.%Y %H:%M:%S"),
                escape("{0}".format(item.price)),
                escape("{0}".format(item.get_initiator_type_display()))

            ])
        return json_data

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        qs_params = None
        date_from = self.request.GET.get('date_from', None)
        date_to = self.request.GET.get('date_to', None)

        if search:
            search_parts = search.split('?')

            for part in search_parts:
                q = Q(id__istartswith=part)|\
                    Q(card__data__istartswith=part)|\
                    Q(partner__name__istartswith=part)|\
                    Q(station__owner__istartswith=part)|\
                    Q(post__id__istartswith=part)|\
                    Q(price__istartswith=part)

                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)

        if date_from:
            print(datetime.strptime(date_from, "%d.%m.%Y"))
            q = Q(start_time__gte=datetime.strptime(date_from, "%d.%m.%Y"))
            qs_params = qs_params & q if qs_params else q

            qs = qs.filter(qs_params)

            
        if date_to:
            print(datetime.strptime(date_to, "%d.%m.%Y"))
            q = Q(start_time__lte=datetime.strptime(date_to, "%d.%m.%Y"))
            qs_params = qs_params & q if qs_params else q

            qs = qs.filter(qs_params)

        return qs