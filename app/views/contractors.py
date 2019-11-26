from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from app.utils import ObjectListMixin, objectDetailRequest, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from app.models import Contractor
from app.forms import ContractorForm


class ContractorList(LoginRequiredMixin, ObjectListMixin, View):
    model = Contractor
    template = 'app/contractor/contractor_list.html'
    context = 'contractors'


class ContractorCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = ContractorForm
    template = 'app/contractor/contractor_create.html'
    # Urls names is in urls.py
    redirect_url = 'contractor_list_url'


class ContractorUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Contractor
    model_form = ContractorForm
    template = 'app/contractor/contractor_update.html'


class ContractorDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Contractor
    template = 'app/contractor/contractor_delete.html'


def contractorDetailRequest(request):
    model = Contractor
    template = 'app/contractor/contractor_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))