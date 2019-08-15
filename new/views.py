from django.shortcuts import render, redirect
from django.views.generic import View
from .models import *
from .forms import *
from .mqtt.publisher import publish_data
import json

# Create your views here.
class TransactionList(View):
    def get(self, request):
        transactions = Transaction.objects.all()
        # form = TestMessageForm
        return render(request, 'app/transaction_list.html', context={'transactions': transactions})
    
    def post(self, request):
        # bound_form = TestMessageForm(request.POST)
        # if bound_form.is_valid():
        dst="0A1B2C3D4E5F"
        data={"client":0x0A1B2C3D4E5F60,"payment":1}
        publish_data(dst,json.dumps(data))
        return redirect("/")


class PartnerList(View):
    def get(self, request):
        partners = Partner.objects.all()
        return render(request, 'app/partner_list.html', context={'partners': partners})


class ContractorList(View):
    def get(self, request):
        contractors = Contractor.objects.all()
        return render(request, 'app/contractor_list.html', context={'contractors': contractors})


class CardList(View):
    def get(self, request):
        cards = Card.objects.all()
        return render(request, 'app/card_list.html', context={'cards': cards})

class StationList(View):
    def get(self, request):
        stations = Station.objects.all()
        return render(request, 'app/station_list.html', context={'stations': stations})


class PartnerCreate(View):
    
    def get(self, request):
        form = PartnerForm
        return render(request, 'app/partner_create.html', context={'form': form})
    
    def post(self, request):
        bound_form = PartnerForm(request.POST)
        if bound_form.is_valid():
            new_partner = bound_form.save()
            return redirect('/partners')
        # return render(request, context={'form': bound_form})

class ContractorCreate(View):
    
    def get(self, request):
        form = ContractorForm
        return render(request, 'app/contractor_create.html', context={'form': form})
    
    def post(self, request):
        bound_form = ContractorForm(request.POST)
        if bound_form.is_valid():
            new_contractor = bound_form.save()
            return redirect('/contractors')