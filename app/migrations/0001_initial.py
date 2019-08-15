# Generated by Django 2.2 on 2019-04-19 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=200, verbose_name='Данные карты')),
            ],
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название организации контрагента')),
                ('UNP', models.CharField(max_length=50, verbose_name='УНП')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
                ('balance', models.PositiveIntegerField(verbose_name='Баланс')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название организации партнера')),
                ('identification_type', models.PositiveSmallIntegerField(choices=[(1, 'Госномер'), (2, 'ФИО'), (3, 'УНП'), (4, 'ТС')], default=1, verbose_name='Тип идентификации')),
                ('data', models.CharField(max_length=200, verbose_name='Данные партнера')),
                ('balance', models.PositiveIntegerField(verbose_name='Баланс')),
                ('contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partners', to='app.Contractor', verbose_name='Контрагент')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=50, verbose_name='Владелец')),
                ('ip', models.GenericIPAddressField(verbose_name='IP адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')),
                ('price', models.PositiveSmallIntegerField(verbose_name='Цена')),
                ('initiator_type', models.PositiveSmallIntegerField(choices=[(1, 'ПО'), (2, 'Контроллер'), (3, 'Другое')], default=1, verbose_name='Инициатор транзакции')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.Card', verbose_name='Карта')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.Partner', verbose_name='Партнер')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.Post', verbose_name='Пост')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='app.Station', verbose_name='Станция')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app.Station', verbose_name='Пост'),
        ),
        migrations.AddField(
            model_name='card',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='app.Partner', verbose_name='Партнер'),
        ),
    ]
