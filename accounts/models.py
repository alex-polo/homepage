from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class ApplicationUser(AbstractUser):
    family_name = models.CharField(verbose_name='Фамилия', max_length=150)
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Отчетство', max_length=150)

    def save(self, *args, **kwargs):
        super(ApplicationUser, self).save(*args, **kwargs)

    def __str__(self):
        # return f'{self.username} | {self.first_name} {self.last_name} {self.family_name}'
        return self.username

    class Meta:
        db_table = 'xxt_accounts_application_users'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'


class ApplicationUsersGroup(Group):
    pass

    class Meta:
        db_table = 'xxt_accounts_application_group'
        verbose_name = 'Группу пользователей'
        verbose_name_plural = 'Группы пользователей'
