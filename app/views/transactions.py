import pytz

from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.conf import settings
from django.utils.html import escape

from app.models import Transaction
from app.utils import ObjectListMixin

# View for render transaction page. See utils.py
class TransactionList(LoginRequiredMixin, ObjectListMixin, View):
    model = Transaction
    template = 'app/transaction/transaction_list.html'
    context = 'transactions'

# Get raw table data.
class TransactionListJson(LoginRequiredMixin, BaseDatatableView):
    model = Transaction
    columns = ['id', 'card', 'partner',
               'station', 'post', 'start_time', 'price', 'initiator_type']
    order_columns = ['id', 'card', 'partner',
               'station', 'post', 'start_time', 'price', 'initiator_type']

    def get_initial_queryset(self):
        filter_key = self.request.GET.get('filter_key', None)
        qs_params = None

        if filter_key:
            q = Q(id__istartswith=filter_key) |\
                Q(partner__contractor__name__istartswith=filter_key)|\
                Q(card__data__istartswith=filter_key) |\
                Q(partner__name__istartswith=filter_key) |\
                Q(station__owner__istartswith=filter_key) |\
                Q(post__id__istartswith=filter_key) |\
                Q(price__istartswith=filter_key)
            qs_params = qs_params & q if qs_params else q
            return Transaction.objects.filter(qs_params)
        else:
            return Transaction.objects.filter()
   
    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        tz = pytz.timezone(settings.TIME_ZONE)

        for item in qs:
            if item.card:
                new_card = item.card.name
            else:
                new_card = "Нет карты"
            if item.partner:
                new_partner = item.partner.name
            else:
                new_partner = "Нет партнера"
            if item.start_time:
                item.start_time = tz.normalize(item.start_time)
            
            json_data.append([
                escape(item.id),
                escape("{0}".format(new_card)),
                escape("{0}".format(new_partner)),
                escape("{0}".format(item.station.owner)),
                escape("{0}".format(item.post.post_id)),
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
        search_column_filter = ""
        filter_columns_name = {}
        filter_columns = ['id','card__name', 'partner__name', 'station__owner', 'post__post_id', 'start_time', 'price', 'initiator_type']
        filter_query =""

        for i in range(len(filter_columns)):
            search_column_filter = self.request.GET.get("columns[{}][search][value]".format(i))
            if search_column_filter:
                filter_columns_name[filter_columns[i].lower()] = search_column_filter

        if filter_columns_name.values():
            for column, value in filter_columns_name.items():
                for value in value.split():
                    if column == "post__post_id" or column == "price":
                        filter_query = { "{}".format(column): value }
                    else:
                        filter_query = { "{}__icontains".format(column): value }
                    q = Q(**filter_query)
                    qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params) 
           
        if search:
            search_parts = search.split()
            for part in search_parts:
                q = Q(id__icontains=part) |\
                    Q(card__name__icontains=part) |\
                    Q(partner__name__icontains=part) |\
                    Q(station__owner__icontains=part) |\
                    Q(post__post_id__icontains=part) |\
                    Q(price__icontains=part)
                qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)

        if date_from:
            q = Q(start_time__gte=datetime.strptime(date_from, "%d.%m.%Y"))
            qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)

        if date_to:
            q = Q(start_time__lte=datetime.strptime(date_to, "%d.%m.%Y"))
            qs_params = qs_params & q if qs_params else q
            qs = qs.filter(qs_params)
        return qs
