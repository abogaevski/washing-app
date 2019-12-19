# Generated by Django 2.2 on 2019-12-19 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_epospayment_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='initiator_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Контроллер'), (1, 'Веб-приложение'), (2, 'Купюроприемник'), (4, 'EPOS платеж')], default=1, verbose_name='Инициатор транзакции'),
        ),
    ]