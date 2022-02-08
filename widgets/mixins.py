import logging
from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from hm_settings.models import HomepageSettings
from widgets.models import PageWidgets, WidgetsGroups, MemoryWidgets, TypeBrowser, LinkWidgets

logger = logging.getLogger('server')


def _get_settings_value(property_attr: str) -> Optional[str]:
    return HomepageSettings.objects.get(property_attribute=property_attr).property_value


def _get_page_settings(name_page: str):
    return PageWidgets.objects.get(const_sys_property=name_page)


def _get_default_context_page_meta():
    """Метод вызывется в случае ошибки при получении данных из бд"""
    value = 'Unknown'
    return {
        'name_application': 'Homepage',
        'search_field_value': value,
        'title': value,
        'header': value,
        'name_page': value,
    }


def _get_all_types_browsers():
    """Возвращает все типы браузеров из бд"""
    return TypeBrowser.objects.all()


def _get_link_widgets(widgets_groups, browser_type, search_keywords):
    """Возвращает список ссылочных виджетов согласно заданным параметрам"""
    if search_keywords is not None and len(search_keywords) > 0:
        return [link_widget for link_widget in LinkWidgets.objects.filter(is_active=True,
                                                                          widgets_groups=widgets_groups,
                                                                          browser_type__in=browser_type).values()
                if search_keywords.lower() in link_widget.get('name').lower()]
    else:
        return list(LinkWidgets.objects.filter(is_active=True, widgets_groups=widgets_groups,
                                               browser_type__in=browser_type).values())


def _get_memory_widgets(widgets_groups, browser_type, search_keywords):
    """Возвращает список пямяток согласно заданным параметрам"""
    if search_keywords is not None and len(search_keywords) > 0:
        return [memory_widget for memory_widget in
                MemoryWidgets.objects.filter(is_active=True, widgets_groups=widgets_groups,
                                             browser_type__in=browser_type).values()
                if search_keywords.lower() in memory_widget.get('name').lower()]
    else:
        return list(MemoryWidgets.objects.filter(is_active=True, widgets_groups=widgets_groups,
                                                 browser_type__in=browser_type).values())


def _get_page(name_page: str):
    return PageWidgets.objects.get(const_sys_property=name_page)


def _get_widget_groups_for_anonymous_user(page):
    return WidgetsGroups.objects.filter(page=page)


def _get_widgets_groups_for_user(page: QuerySet, user_groups) -> QuerySet:
    return WidgetsGroups.objects.filter(page=page, access_group__in=user_groups)


class LibraryPageMixin:
    """Создан для медиа библиотеки, которая пока не добавлена на сайт"""
    template_name = None
    name_page = None

    @classmethod
    def page_meta(cls):
        context_page_meta = {}
        try:
            logger.debug(f'Start LibraryPageMixin, name page: {cls.name_page}, method: page_meta')
            context_page_meta['name_application'] = _get_settings_value('name_application')
            context_page_meta['search_field_value'] = _get_settings_value('search_field_value')
            context_page_meta['title'] = _get_settings_value('title_media_library_page')
            context_page_meta['header'] = _get_settings_value('header_media_library_page')
            context_page_meta['name_page'] = cls.name_page
            logger.debug('End LibraryPageMixin, method: page_meta')
        except Exception as error:
            context_page_meta = _get_default_context_page_meta()
            logger.error(error)
        finally:
            logger.debug('LibraryPageMixin return context_page_meta')
            return context_page_meta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.page_meta())
        return context


class HomePageMixin:
    """
    Метод отдает контекст страниц страниц сайта shared_page и private_page.
    Страницы отдаются без списка виджетов.
    """
    template_name = None
    name_page = None

    @classmethod
    def page_meta(cls):
        context_page_meta = {}
        try:
            logger.debug(f'Start HomePageMixin, name page: {cls.name_page}, method: page_meta')
            page = _get_page_settings(cls.name_page)
            context_page_meta['name_application'] = _get_settings_value('name_application')
            context_page_meta['search_field_value'] = _get_settings_value('search_field_value')
            context_page_meta['title'] = page.title
            context_page_meta['header'] = page.header
            context_page_meta['name_page'] = cls.name_page
            logger.debug('End HomePageMixin, method: page_meta')
        except Exception as error:
            context_page_meta = _get_default_context_page_meta()
            logger.error(error)
        finally:
            logger.debug('HomePageMixin return context_page_meta')
            return context_page_meta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.page_meta())
        return context


class MemoryWidgetsMixin:

    @classmethod
    def response_context(cls, request, pk):
        logger.debug('Start method get in class MemoryWidgetsMixin')
        user = request.user
        page = PageWidgets.objects.get(const_sys_property='shared_page')
        logger.debug('Getting shared_page')
        query_set_widgets_groups = WidgetsGroups.objects.all()
        anon_card_group = query_set_widgets_groups.filter(page=page)
        logger.debug(f'Find shared widgets groups: {list(anon_card_group)}')
        logger.debug(f'Find user: {user}')

        if request.user.is_anonymous is False and user.is_active:
            logger.debug(f'User {user} is authenticated')
            user_groups = user.groups.all()
            logger.debug(f'Find user groups: {user_groups}')
            user_widgets_groups = WidgetsGroups.objects.filter(access_group__in=user_groups)
            logger.debug(f'Find widgets groups: {list(user_widgets_groups)}')
            anon_and_user_widgets_groups = anon_card_group | user_widgets_groups
            memory_card = get_object_or_404(MemoryWidgets, id=pk, widgets_groups__in=anon_and_user_widgets_groups)
        else:
            logger.debug('User is not authenticated')
            memory_card = get_object_or_404(MemoryWidgets, id=pk, widgets_groups__in=anon_card_group)

        logger.debug('Next step return memory cards value')
        value = {'name': memory_card.name, 'content': memory_card.content}
        return value


class BaseWidgetsMixin:
    """Базовый класс для SharedWidgetsMixin и PrivateWidgetMixin"""
    name_page = None
    page = None
    search_keywords = None
    http_user_agent = None
    type_browsers = None
    widgets_groups = None

    @classmethod
    def define_browsers(cls, http_user_agent: str) -> list:
        return [type_browser for type_browser in _get_all_types_browsers()
                if type_browser.attribute in http_user_agent or type_browser.attribute == 'all']

    def define_request_data(self, request: WSGIRequest):

        self.search_keywords = request.GET.get('search')
        self.http_user_agent = request.META['HTTP_USER_AGENT']
        self.type_browsers = self.define_browsers(self.http_user_agent)
        self.page = _get_page(self.name_page)

    def filtering_widgets(self) -> dict:
        list_widgets = []

        for group in self.widgets_groups:
            widgets = _get_link_widgets(widgets_groups=group, browser_type=self.type_browsers,
                                        search_keywords=self.search_keywords)
            widgets.extend(_get_memory_widgets(widgets_groups=group, browser_type=self.type_browsers,
                                               search_keywords=self.search_keywords))

            if len(widgets) > 0:
                list_widgets.append({group.show_name: widgets})

        response = {'success': True, 'list_widgets': list_widgets}
        return response
        # if self.search_keywords is not None and len(self.search_keywords) > 0:
        #     pass
        # else:
        #     pass


class WidgetsMixin(BaseWidgetsMixin):
    """
    Данный миксин обслуживает запросы на получение виджетов пришедшие от зарегистрированных пользователей
    """

    def get(self, request):
        try:
            super().define_request_data(request)
            self.widgets_groups = _get_widget_groups_for_anonymous_user(self.page)
            return JsonResponse(self.filtering_widgets())
        except Exception as error:
            logger.error(error)
            response = {'success': False, 'message': str(error)}
            logger.debug(f'response: {response}')
            return JsonResponse(response)


class PrivateWidgetsMixin(BaseWidgetsMixin):
    """
    Обслуживает запросы на получение виджетов пришедшие от зарегистрированных пользователей
    """
    def get(self, request, **kwargs):
        try:
            logger.debug('Start method get in class PrivateCardsMixin')
            user = request.user
            if request.user.is_anonymous is False and user.is_active:
                super().define_request_data(request)
                self.widgets_groups = _get_widgets_groups_for_user(page=self.page, user_groups=user.groups.all())
                response = self.filtering_widgets()
                return JsonResponse(response)
            else:
                logger.debug(f'User is not authenticated')
                response = {'success': False, 'message': 'user is not authenticated'}
                logger.debug(f'response: {response}')
                return JsonResponse(response)
        except Exception as error:
            logger.error(error)
            response = {'success': False, 'message': str(error)}
            logger.debug(f'response: {response}')
            return JsonResponse(response)
