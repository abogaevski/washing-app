# Generated by Django 2.2 on 2019-05-14 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_testmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uid',
            field=models.IntegerField(default=0, verbose_name='UID'),
        ),
    ]
