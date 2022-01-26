from django.db import models


class HomepageSettings(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.CharField(verbose_name='Свойство', max_length=200, unique=True)
    property_attribute = models.CharField(verbose_name='Системное имя', max_length=200, unique=True)
    property_value = models.CharField(verbose_name='Значение свойства', max_length=200, unique=False)

    def __str__(self):
        return self.property

    class Meta:
        db_table = 'xxt_homepage_settings'
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'
