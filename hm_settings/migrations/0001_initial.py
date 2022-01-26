# Generated by Django 3.2.9 on 2022-01-26 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainConstProperty',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('property', models.CharField(max_length=200, unique=True, verbose_name='Свойство')),
                ('property_attribute', models.CharField(max_length=200, unique=True, verbose_name='Системное имя')),
                ('property_value', models.CharField(max_length=200, verbose_name='Значение свойства')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
                'db_table': 'xxt_settings',
            },
        ),
    ]
