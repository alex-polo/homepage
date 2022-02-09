# Generated by Django 4.0.1 on 2022-02-09 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='linkwidgets',
            options={'ordering': ['index_number'], 'verbose_name': 'Ссылку', 'verbose_name_plural': 'Ссылки'},
        ),
        migrations.AlterModelOptions(
            name='memorywidgets',
            options={'ordering': ['index_number'], 'verbose_name': 'Памятку', 'verbose_name_plural': 'Памятки'},
        ),
        migrations.AlterModelOptions(
            name='typebrowser',
            options={'verbose_name': 'Тип браузера', 'verbose_name_plural': 'Виды браузера'},
        ),
        migrations.AlterModelOptions(
            name='widgetsgroups',
            options={'ordering': ['index_number'], 'verbose_name': 'Группу виджетов', 'verbose_name_plural': 'Группы виджетов'},
        ),
        migrations.RemoveField(
            model_name='widgetsgroups',
            name='access_group',
        ),
        migrations.AddField(
            model_name='widgetsgroups',
            name='access_group',
            field=models.ManyToManyField(to='auth.Group', verbose_name='Группы пользователей'),
        ),
    ]