from django.db import models
from django.contrib.auth.models import Group


class PageWidgets(models.Model):
    id = models.AutoField(primary_key=True)
    name_page = models.CharField(max_length=255, unique=True, verbose_name='Название страницы')
    description = models.CharField(verbose_name='Описание', max_length=255, unique=False, blank=True)
    title = models.CharField(max_length=80, unique=False, verbose_name='Title')
    header = models.CharField(max_length=50, unique=False, verbose_name='Заголовок страницы')
    const_sys_property = models.CharField(max_length=50, unique=False, verbose_name='sys_property')
    last_update_date = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    def __str__(self):
        return self.name_page

    class Meta:
        db_table = 'xxt_widgets_page'
        ordering = ['name_page']
        verbose_name = 'Страницу'
        verbose_name_plural = 'Страницы'


class WidgetsGroups(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название группы', max_length=200, unique=False)
    show_name = models.CharField(verbose_name='Отображаемое имя на странице', max_length=200, unique=False, default='')
    description = models.CharField(verbose_name='Описание', max_length=255, unique=False, blank=True)
    page = models.ForeignKey(PageWidgets, on_delete=models.PROTECT, null=True, verbose_name='Страница')
    index_number = models.IntegerField(verbose_name='Порядок вывода')
    access_group = models.ManyToManyField(Group, verbose_name='Группы пользователей', blank=True)
    last_update_date = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'xxt_widgets_groups'
        ordering = ['index_number']
        verbose_name = 'Группу виджетов'
        verbose_name_plural = 'Группы виджетов'


class TypeBrowser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Название браузера', max_length=120, unique=True)
    attribute = models.CharField(verbose_name='Строка из User-Agent', max_length=255, unique=True)
    last_update_date = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    @property
    def browser(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'xxt_widgets_type_browsers'
        verbose_name = 'Тип браузера'
        verbose_name_plural = 'Виды браузера'


class MemoryWidgets(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Включена', default=False)
    index_number = models.IntegerField(verbose_name='Порядок вывода')
    name = models.CharField(verbose_name='Наименование', max_length=200, unique=False)
    content = models.TextField(verbose_name='Текст памятки', max_length=255, unique=False, null=True)
    type = models.CharField(max_length=50, default='memory_widget')
    browser_type = models.ManyToManyField(TypeBrowser, verbose_name='Браузеры')
    widgets_groups = models.ManyToManyField(WidgetsGroups, verbose_name='Группа')
    last_update_date = models.DateTimeField(verbose_name='Дата последнего обновления записи', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'xxt_widgets_memory'
        ordering = ['index_number']
        verbose_name = 'Памятку'
        verbose_name_plural = 'Памятки'


class LinkWidgets(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(verbose_name='Включена', default=False)
    index_number = models.IntegerField(verbose_name='Порядок вывода')
    name = models.CharField(verbose_name='Наименование', max_length=200, unique=False)
    url = models.URLField(verbose_name='URL', max_length=255)
    type = models.CharField(max_length=50, default='link_widget')
    browser_type = models.ManyToManyField(TypeBrowser, verbose_name='Браузеры')
    widgets_groups = models.ManyToManyField(WidgetsGroups, verbose_name='Группа')
    last_update_date = models.DateTimeField(verbose_name='Дата последнего обновления записи', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'xxt_widgets_link'
        ordering = ['index_number']
        verbose_name = 'Ссылку'
        verbose_name_plural = 'Ссылки'
