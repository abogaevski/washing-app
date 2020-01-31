from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from app.utils import ObjectListMixin, objectDetailRequest, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin, ObjectDetailMixin
from app.models import Partner, UserTransaction
from app.forms import PartnerForm, PartnerCoinForm

class PartnerList(LoginRequiredMixin, ObjectListMixin, View):
    model = Partner
    template = 'app/partner/partner_list.html'
    context = 'partners'


class PartnerCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = PartnerForm
    template = 'app/partner/partner_create.html'
    # Urls names is in urls.py
    redirect_url = 'partner_list_url'


class PartnerUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Partner
    model_form = PartnerForm
    template = 'app/partner/partner_update.html'


class PartnerDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Partner
    template = 'app/partner/partner_delete.html'


@method_decorator(staff_member_required(login_url='login_url'), name='get')
@method_decorator(staff_member_required(login_url='login_url'), name='post')
class PartnerAddCoins(LoginRequiredMixin, View):
    def get(self, request, id):
        partner = Partner.objects.get(id=id)
        bound_form = PartnerCoinForm(instance=partner)

        return render(request, 'app/partner/partner_add_coins.html',
                      context={'form': bound_form,
                               'partner': partner})
    def post(self, request, id):
        partner = Partner.objects.get(id=id)
        bound_form = PartnerCoinForm(request.POST, instance=partner)
        partner_balance = partner.balance

        if bound_form.is_valid():
            contractor_balance = partner.contractor.balance
            partner_balance_in_form = bound_form.cleaned_data['balance']
            message = 'Изменение баланса клиента. '
            if partner_balance_in_form > contractor_balance:
                message += 'Ошибка. Вы указали баланс больше, чем имеется у контрагента.\
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
                message += 'Успешно. Добавлено ' + \
                    str(partner_balance_in_form) + ' к ' + new_partner_obj.name

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

    
def partnerDetailRequest(request):
    model = Partner
    template = 'app/partner/partner_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))


# TODO: Create one mixin
@staff_member_required(login_url='login_url')
def partnerAddCoinsRequest(request):
    if request.is_ajax():
        post = request.POST
        bound_balance = {
            'balance': post['balance']
        }

        partner = Partner.objects.get(id=post['item'])
        partner_balance = partner.balance

        bound_form = PartnerCoinForm(bound_balance, instance=partner)
        message = "Изменение баланса клиента. "

        if bound_form.is_valid():
            contractor_balance = partner.contractor.balance
            partner_balance_in_form = bound_form.cleaned_data['balance']

            if partner_balance_in_form > contractor_balance:
                message += "Ошибка! Вы добавили больше, чем имеется у контрагента"

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=0,
                    amount=partner_balance_in_form
                )

                return JsonResponse({"message": message, "class": "alert-warning", 'partner': partner.id})

            elif (partner_balance + partner_balance_in_form) < 0:

                message += "Ошибка. У партнера не может быть меньше нуля"
                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=0,
                    amount=partner_balance_in_form
                )
                return JsonResponse({"message": message, "class": "alert-warning", 'partner': partner.id})

            else:
                contractor = partner.contractor
                new_contractor_balance = contractor_balance - partner_balance_in_form
                contractor.balance = new_contractor_balance
                contractor.save()

                new_partner_balance = partner_balance + partner_balance_in_form
                new_partner_obj = bound_form.save(commit=False)
                new_partner_obj.balance = new_partner_balance
                new_partner_obj.save()

                message += 'Успешно. Добавлено ' + \
                    str(partner_balance_in_form) + ' к ' + new_partner_obj.name

                UserTransaction.objects.create(
                    entity='Клиент: ' + partner.name,
                    user=request.user,
                    annotation=message,
                    exec_type=1,
                    amount=partner_balance_in_form
                )

                return JsonResponse({"message": message, "class": "alert-success", 'new_balance': new_partner_balance, 'new_contractor_balance': new_contractor_balance, 'partner': partner.id})
        message += "Произошла ошибка!"

        UserTransaction.objects.create(
            entity='Клиент: ' + partner.name,
            user=request.user,
            annotation=message,
            exec_type=1,
            amount=partner_balance_in_form
        )
        return JsonResponse({"message": message + str(bound_form.errors), "class": "alert-danger", 'partner': partner.id})


class PartnerDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Partner
    template = "app/partner/partner_detail_page.html"