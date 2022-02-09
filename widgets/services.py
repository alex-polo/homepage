from typing import Optional

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from hm_settings.models import HomepageSettings
from widgets.models import PageWidgets, TypeBrowser, WidgetsGroups, MemoryWidgets, LinkWidgets


def get_settings_value(property_attr: str) -> Optional[str]:
    """Возвращает значение свойства из таблицы xxx_hm_settings"""
    return HomepageSettings.objects.get(property_attribute=property_attr).property_value


def get_default_context_page_meta() -> dict:
    """Метод вызывется в случае ошибки при получении данных из бд"""
    value = 'Unknown'
    return {
        'name_application': 'Homepage',
        'search_field_value': value,
        'title': value,
        'header': value,
        'name_page': value,
    }


def get_all_types_browsers() -> QuerySet:
    """Возвращает все типы браузеров из бд"""
    return TypeBrowser.objects.all()


def get_widgets_with_keyword(widgets_groups: QuerySet, browser_type: list, search_keywords: str) -> list:
    """Возвращает список виджетов согласно заданного ключевого слова в поиске"""
    widgets = [link_widget for link_widget in LinkWidgets.objects.filter(is_active=True,
                                                                         widgets_groups=widgets_groups,
                                                                         browser_type__in=browser_type).values()
               if search_keywords.lower() in link_widget.get('name').lower()]

    widgets.extend(
        [memory_widget for memory_widget in
         MemoryWidgets.objects.filter(is_active=True,
                                      widgets_groups=widgets_groups,
                                      browser_type__in=browser_type).values()
         if search_keywords.lower() in memory_widget.get('name').lower()]
    )

    return widgets


def get_widgets(widgets_groups: QuerySet, browser_type: list) -> list:
    """Возвращает список виджетов согласно переданным групп виджетов и типу браузера"""
    widgets = list(LinkWidgets.objects.filter(is_active=True, widgets_groups=widgets_groups,
                                              browser_type__in=browser_type).values())
    widgets.extend(list(MemoryWidgets.objects.filter(is_active=True, widgets_groups=widgets_groups,
                                                     browser_type__in=browser_type).values()))
    return widgets


def get_page(name_page: str) -> QuerySet:
    """Отдает страницу согласно полученного name_page"""
    return PageWidgets.objects.get(const_sys_property=name_page)


def get_widget_groups_for_shared_page(page: QuerySet) -> QuerySet:
    """Отдает список групп виджетов для страницы shared_page. Сделано для главной страницы сайта"""
    return WidgetsGroups.objects.filter(page=page)


def get_widgets_groups_for_user(page: QuerySet, user_groups: QuerySet) -> QuerySet:
    """Возвращает список групп виджетов для страницы private_page согласно переданным группам безопасности,
    в которых состоит пользователь"""
    return WidgetsGroups.objects.filter(page=page, access_group__in=user_groups)


def get_memory_widget(pk: int, widget_groups: QuerySet) -> QuerySet:
    """Возвращает конкретный виджет по id"""
    return get_object_or_404(MemoryWidgets, id=pk, widgets_groups__in=widget_groups)
