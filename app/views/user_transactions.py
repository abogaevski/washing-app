from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from app.utils import ObjectListMixin
from app.models import UserTransaction


class UserTransactionList(LoginRequiredMixin, ObjectListMixin, View):
    model = UserTransaction
    template = 'app/user_transaction/user_transaction_list.html'
    context = 'transactions'