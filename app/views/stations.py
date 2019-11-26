from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from app.utils import ObjectListMixin, objectDetailRequest, ObjectCreateMixin, ObjectUpdateMixin
from app.models import Station
from app.forms import StationForm


class StationList(LoginRequiredMixin, ObjectListMixin, View):
    model = Station
    template = 'app/station/station_list.html'
    context = 'stations'


def stationDetailRequest(request):
    model = Station
    template = 'app/station/station_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))


class StationCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = StationForm
    template = 'app/station/station_create.html'
    # Urls names is in urls.py
    redirect_url = 'station_list_url'


class StationUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Station
    model_form = StationForm
    template = 'app/station/station_update.html'