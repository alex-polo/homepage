# Generated by Django 3.2.9 on 2022-01-26 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hm_settings', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MainConstProperty',
            new_name='HomepageSettings',
        ),
        migrations.AlterModelTable(
            name='homepagesettings',
            table='xxt_homepage_settings',
        ),
    ]