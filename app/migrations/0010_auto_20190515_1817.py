# Generated by Django 2.2 on 2019-05-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20190515_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mac_uid',
            field=models.CharField(max_length=12, unique=True, verbose_name='MAC UID'),
        ),
    ]
