# Generated by Django 2.2 on 2019-11-18 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20190814_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='name',
            field=models.CharField(default='Карта', max_length=100, verbose_name='Название карты'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partner',
            name='data',
            field=models.CharField(max_length=200, verbose_name='Данные клиента'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название клиента'),
        ),
    ]
