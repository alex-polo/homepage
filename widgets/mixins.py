import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from widgets import services

logger = logging.getLogger('server')


class LibraryPageMixin:
    """Создан для медиа библиотеки, которая пока не добавлена на сайт"""
    template_name = None
    name_page = None

    @classmethod
    def page_meta(cls):
        context_page_meta = {}
        try:
            logger.debug(f'Start LibraryPageMixin, name page: {cls.name_page}, method: page_meta')
            context_page_meta['name_application'] = services.get_settings_value('name_application')
            context_page_meta['search_field_value'] = services.get_settings_value('search_field_value')
            context_page_meta['title'] = services.get_settings_value('title_media_library_page')
            context_page_meta['header'] = services.get_settings_value('header_media_library_page')
            context_page_meta['name_page'] = cls.name_page
        except Exception as error:
            context_page_meta = services.get_default_context_page_meta()
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
            logger.debug(f'HomePageMixin, name page: {cls.name_page}, method: page_meta')
            page = services.get_page(cls.name_page)
            context_page_meta['name_application'] = services.get_settings_value('name_application')
            context_page_meta['search_field_value'] = services.get_settings_value('search_field_value')
            context_page_meta['title'] = page.title
            context_page_meta['header'] = page.header
            context_page_meta['name_page'] = cls.name_page
        except Exception as error:
            context_page_meta = services.get_default_context_page_meta()
            logger.error(error)
        finally:
            logger.debug('HomePageMixin return context_page_meta')
            return context_page_meta

    def get_context_data(self, **kwargs):
        logger.debug(f'HomePageMixin, name page: {self.name_page}, method: get_context_data')
        context = super().get_context_data(**kwargs)
        context.update(self.page_meta())
        return context


class MemoryWidgetsMixin:

    @classmethod
    def response_context(cls, request, pk):
        logger.debug('Start method response_context in class MemoryWidgetsMixin')
        user = request.user
        anon_card_group = services.get_widget_groups_for_shared_page(page=services.get_page('shared_page'))

        if user.is_anonymous is False and user.is_active:
            logger.debug(f'Is authenticated user {user} getting memory widget')
            user_widgets_groups = services.get_widgets_groups_for_user(page=services.get_page('private_page'),
                                                                       user_groups=user.groups.all())
            memory_card = services.get_memory_widget(pk=pk, widget_groups=anon_card_group | user_widgets_groups)
        else:
            logger.debug('Is not authenticated user getting memory widget')
            memory_card = services.get_memory_widget(pk=pk, widget_groups=anon_card_group)

        return {'name': memory_card.name, 'content': memory_card.content}


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
        logger.debug('BaseWidgetsMixin, start method define_browsers')
        return [type_browser for type_browser in services.get_all_types_browsers()
                if type_browser.attribute in http_user_agent or type_browser.attribute == 'all']

    def define_request_data(self, request: WSGIRequest):
        logger.debug('BaseWidgetsMixin, start method define_request_data')
        self.search_keywords = request.GET.get('search')
        self.http_user_agent = request.META['HTTP_USER_AGENT']
        self.type_browsers = self.define_browsers(self.http_user_agent)
        self.page = services.get_page(self.name_page)

    def filtering_widgets(self) -> dict:
        logger.debug('BaseWidgetsMixin, start method filtering_widgets')
        list_widgets = []

        for group in self.widgets_groups:
            if self.search_keywords is not None and len(self.search_keywords) > 0:
                widgets = services.get_widgets_with_keyword(widgets_groups=group, browser_type=self.type_browsers,
                                                            search_keywords=self.search_keywords)
            else:
                widgets = services.get_widgets(widgets_groups=group, browser_type=self.type_browsers)

            if len(widgets) > 0:
                list_widgets.append({group.show_name: widgets})

        response = {'success': True, 'list_widgets': list_widgets}
        return response


class WidgetsMixin(BaseWidgetsMixin):
    """
    Данный миксин обслуживает запросы на получение виджетов пришедшие от зарегистрированных пользователей
    """

    def get(self, request):
        logger.debug('WidgetsMixin, start method get')
        try:
            super().define_request_data(request)
            self.widgets_groups = services.get_widget_groups_for_shared_page(self.page)
            return JsonResponse(self.filtering_widgets())
        except Exception as error:
            logger.error(error)
            response = {'success': False, 'message': str(error)}
            logger.debug(f'response: {response}')
            return JsonResponse(response)


class PrivateWidgetsMixin(BaseWidgetsMixin):
    """
    Обслуживает запросы на получение виджетов пришедшие от зарегистрированных пользователей на странице private_page
    """
    def get(self, request, **kwargs):
        try:
            logger.debug('PrivateWidgetsMixin, start method get')
            user = request.user
            if request.user.is_anonymous is False and user.is_active:
                super().define_request_data(request)
                self.widgets_groups = services.get_widgets_groups_for_user(page=self.page,
                                                                           user_groups=user.groups.all())
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
