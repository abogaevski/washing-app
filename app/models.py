from decimal import *

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import messages
from django.urls import reverse


# Create your models here.
class Contractor(models.Model):
    name = models.CharField("Название организации контрагента", max_length=100, db_index=True)
    UNP = models.CharField("УНП", max_length=50)
    address = models.CharField("Адрес", max_length=50)
    balance = models.DecimalField(
        verbose_name="Баланс", max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("contractor_detail_page_url", kwargs={"id": self.pk})


class Partner(models.Model):
    TYPES = (
        (1, 'Госномер'),
        (2, 'ФИО'),
        (3, 'УНП'),
        (4, 'ТС'),
    )
    name = models.CharField("Название клиента", max_length=100, db_index=True)
    identification_type = models.PositiveSmallIntegerField(
        "Тип идентификации", choices=TYPES, default=1)
    data = models.CharField("Данные клиента", max_length=200)
    balance = models.DecimalField(
        verbose_name="Баланс", max_digits=7, decimal_places=2, default=0)
    contractor = models.ForeignKey(
        Contractor, verbose_name="Контрагент", on_delete=models.CASCADE, related_name="partners")

    def __str__(self):
        return str("{} - {}".format(self.contractor.name, self.name))
    
    def get_absolute_url(self):
        return reverse("partner_detail_page_url", kwargs={"id": self.pk})



class Station(models.Model):
    station_id = models.IntegerField('ИД', default=1)
    owner = models.CharField("Владелец", max_length=50)
    course = models.PositiveSmallIntegerField("Курс (балл/руб)", default=1)
    info = models.TextField('Информация', blank=True, max_length=200)
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        return self.owner

    def get_absolute_url(self):
        return reverse("station_detail_page_url", kwargs={"id": self.pk})


class Post(models.Model):
    post_id = models.PositiveSmallIntegerField("Номер поста", default=1, db_index=True)
    station = models.ForeignKey(
        Station, verbose_name='Станция', on_delete=models.CASCADE, related_name="posts")
    mac_uid = models.CharField("MAC UID", max_length=12, unique=True)
    last_seen = models.DateTimeField("Последний раз отвечал")
    is_available = models.BooleanField("Доступность", default=True)
    erip_id = models.CharField("ЕРИП Счет", max_length=100, blank=True)

    def __str__(self):
        return str("{}: Пост {}".format(self.station.owner, self.post_id))
    
    def get_absolute_url(self):
        return reverse("post_detail_page_url", kwargs={"id": self.pk})


class Card(models.Model):
    name = models.CharField("Название карты", max_length=100)
    data = models.CharField('Данные карты', max_length=200, db_index=True)
    partner = models.ForeignKey(
        Partner, verbose_name="Клиент", on_delete=models.CASCADE, related_name="cards")
    is_active = models.BooleanField("Активна", default=True)

    def __str__(self):
        if self.is_active:
            return str("{}: Активна".format(self.data))
        else: 
            return str("{}: Отключена".format(self.data))

    def get_absolute_url(self):
        return reverse("card_detail_page_url", kwargs={"id": self.pk})


class Transaction(models.Model):

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    INIT_TYPES = (
        (0, 'Контроллер'),
        (1, 'Веб-приложение'),
        (2, 'Купюроприемник'),
        (3, 'EPOS платеж')
    )
    card = models.ForeignKey(Card, verbose_name="Карта", on_delete=models.PROTECT,
                             related_name="transactions", blank=True, null=True)
    partner = models.ForeignKey(Partner, verbose_name="Клиент", on_delete=models.PROTECT,
                                related_name="transactions", blank=True, null=True)
    station = models.ForeignKey(Station, verbose_name="Станция",
                                on_delete=models.PROTECT, related_name="transactions")
    post = models.ForeignKey(Post, verbose_name="Пост",
                             on_delete=models.PROTECT, related_name="transactions")
    start_time = models.DateTimeField("Дата начала")
    price = models.DecimalField(
        verbose_name="Цена", max_digits=7, decimal_places=2)
    initiator_type = models.PositiveSmallIntegerField(
        "Инициатор транзакции", choices=INIT_TYPES, default=1)

    def __str__(self):
        return "Транзакция {0}".format(self.pk)


class Payment(models.Model):
    contractor = models.ForeignKey(Contractor, verbose_name="Контрагент",
                                   on_delete=models.PROTECT, related_name="payments", blank=True, null=True)
    amount = models.DecimalField(
        verbose_name="Сумма начисления", max_digits=7, decimal_places=2)
    annotation = models.CharField("Примечание", max_length=150, blank=True)
    date = models.DateTimeField("Дата", auto_now_add=True)

    def __str__(self):
        return self.annotation


class UserTransaction(models.Model):

    EXEC_TYPE = (
        (0, 'Не проведен'),
        (1, 'Проведен'),
    )

    user = models.ForeignKey(User, verbose_name="Пользователь",
                             on_delete=models.PROTECT, related_name="user_transactions")
    entity = models.CharField("Кому", max_length=100)
    annotation = models.CharField("Примечание", max_length=255, blank=True)
    exec_type = models.SmallIntegerField(
        'Статус', choices=EXEC_TYPE, default=0)
    amount = models.DecimalField("Сумма", max_digits=7, decimal_places=2)
    date_pub = models.DateTimeField("Дата", auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField("Эл. почта", blank=True)
    displayname = models.CharField("ФИО", blank=True, max_length=250)
    # phone = 
    is_notify = models.BooleanField("Уведомлять", default=False)

    def __str__(self):
        return self.displayname

    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        
    post_save.connect(create_profile, sender=User)


class EposPayment(models.Model):

    class Meta:
        verbose_name = "Платеж физ. лица"
        verbose_name_plural = "Платежи физ. лиц"

    post = models.ForeignKey(   Post,
                                on_delete=models.PROTECT,verbose_name="Пост",
                                related_name="epos_payments")
    pay_date = models.DateTimeField("Дата платежа")
    amount = models.DecimalField(   verbose_name="Сумма начисления",
                                    max_digits=7, decimal_places=2)
    is_passed = models.BooleanField("Подтвержден", default=False)
    payment_id = models.CharField("ИД платежа", max_length=20, unique=True)
    
    def __str__(self):
        return "{}: {} руб.".format(self.post, self.amount)