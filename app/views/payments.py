from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from app.utils import ObjectListMixin
from app.models import Payment, UserTransaction
from app.forms import PaymentForm

class PaymentList(LoginRequiredMixin, ObjectListMixin, View):
    model = Payment
    template = 'app/payment/payment_list.html'
    context = 'payments'


@method_decorator(staff_member_required(login_url='login_url'), name='get')
@method_decorator(staff_member_required(login_url='login_url'), name='post')
class PaymentCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = PaymentForm
        return render(request, 'app/payment/payment_create.html', context={'form': form})

    def post(self, request):
        message = 'Добавление платежа. '
        bound_form = PaymentForm(request.POST)
        if bound_form.is_valid():
            contractor = bound_form.cleaned_data['contractor']
            amount = bound_form.cleaned_data['amount']
            if contractor:
                contractor.balance += amount
                contractor.save()
            new_obj = bound_form.save()
            message += 'Успешно. Платеж для "' + contractor.name + \
                '" добавлен с примечанием: "' + \
                bound_form.cleaned_data['annotation'] + '"'
            messages.success(request, message)

            UserTransaction.objects.create(
                entity='Контрагент: ' + contractor.name,
                user=request.user,
                annotation=message,
                exec_type=1,
                amount=amount
            )

            return redirect('payment_list_url')

        message += 'Ошибка. Платеж для "' + contractor.name + \
            '" не добавлен с примечанием: "' + \
            bound_form.cleaned_data['annotation'] + '"'
        messages.error(request, message)

        UserTransaction.objects.create(
            entity='Контрагент: ' + contractor.name,
            user=request.user,
            annotation=message,
            exec_type=0,
            amount=amount
        )

        return redirect('payment_list_url')