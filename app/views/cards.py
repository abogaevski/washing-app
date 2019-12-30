from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from app.utils import ObjectListMixin, objectDetailRequest, ObjectCreateMixin, ObjectUpdateMixin, ObjectDisableMixin, ObjectDetailMixin
from app.models import Card
from app.forms import CardForm


class CardList(LoginRequiredMixin, ObjectListMixin, View):
    model = Card
    template = 'app/card/card_list.html'
    context = 'cards'


class CardCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form = CardForm
    template = 'app/card/card_create.html'
    # Urls names is in urls.py
    redirect_url = 'card_list_url'



class CardUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Card
    model_form = CardForm
    template = 'app/card/card_update.html'


class CardDelete(LoginRequiredMixin, ObjectDisableMixin, View):
    model = Card
    template = 'app/card/card_delete.html'


class CardActive(LoginRequiredMixin, View):
    def get(self, request):
        form = CardForm
        return render(request, 'app/card/card_create.html', context={'form': form})

    def post(self, request):
        bound_form = CardForm(request.POST)
        if bound_form.is_valid():
            bound_obj = ''
            try:
                bound_obj = Card.objects.get(
                    data=bound_form.cleaned_data['data'])
            except:
                new_obj = bound_form.save()
                messages.success(request, 'Вы cоздали ' + str(new_obj))
            if bound_obj:
                if not bound_obj.is_active:
                    bound_obj.partner = bound_form.cleaned_data['partner']
                    bound_obj.is_active = True
                    bound_obj.save()
                    messages.success(
                        request, 'Вы включили {0} '.format(bound_obj))
                else:
                    messages.warning(request,   'Вы не можете включить {0}. Уже включена '
                                                .format(bound_obj))
        return redirect('card_list_url')


def cardDetailRequest(request):
    model = Card
    template = 'app/card/card_detail.html'
    return HttpResponse(objectDetailRequest(request, model, template))

class CardDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Card
    template = "app/card/card_detail_page.html"