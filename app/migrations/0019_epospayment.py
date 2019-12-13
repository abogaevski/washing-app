# Generated by Django 2.2 on 2019-12-13 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_delete_epospayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='EposPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_date', models.DateTimeField(verbose_name='Дата платежа')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Сумма начисления')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='epos_payments', to='app.Post', verbose_name='Пост')),
            ],
        ),
    ]