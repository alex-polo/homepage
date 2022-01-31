import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from hm_settings.models import HomepageSettings
from widgets.models import PageWidgets, WidgetsGroups, MemoryWidgets, TypeBrowser, LinkWidgets

logger = logging.getLogger('server')

# User = settings.AUTH_USER_MODEL


class LibraryPageMixin:
    template_name = None
    name_page = None

    @classmethod
    def page_meta(cls):
        context_page_meta = {}
        try:
            logger.debug(f'Start HomePageMixin, name page: {cls.name_page}, method: page_meta')
            context_page_meta['name_application'] = \
                HomepageSettings.objects.get(property_attribute='name_application').property_value

            context_page_meta['search_field_value'] = \
                HomepageSettings.objects.get(property_attribute='search_field_value').property_value

            logger.debug(f"Method: page_meta, name application: {context_page_meta['name_application']}")

            context_page_meta['title'] = \
                HomepageSettings.objects.get(property_attribute='title_media_library_page').property_value
            logger.debug(f"Method: page_meta, title: {context_page_meta['title']}")

            context_page_meta['header'] = \
                HomepageSettings.objects.get(property_attribute='header_media_library_page').property_value
            logger.debug(f"Method: page_meta, header: {context_page_meta['header']}")
            logger.debug('End HomePageMixin, method: page_meta')
            context_page_meta['name_page'] = cls.name_page
        except Exception as error:
            value = 'Unknown'
            context_page_meta['name_application'] = value
            context_page_meta['search_field_value'] = value
            context_page_meta['title'] = value
            context_page_meta['header'] = value
            context_page_meta['name_page'] = value
            logger.error(error)
        finally:
            return context_page_meta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.page_meta())
        return context


class HomePageMixin:
    template_name = None
    name_page = None

    @classmethod
    def page_meta(cls):
        context_page_meta = {}
        try:
            logger.debug(f'Start HomePageMixin, name page: {cls.name_page}, method: page_meta')
            context_page_meta['name_application'] = \
                HomepageSettings.objects.get(property_attribute='name_application').property_value
            logger.debug(f"Method: page_meta, name application: {context_page_meta['name_application']}")

            context_page_meta['search_field_value'] = \
                HomepageSettings.objects.get(property_attribute='search_field_value').property_value
            logger.debug(f"Method: page_meta, search_field_value: {context_page_meta['search_field_value']}")

            logger.debug(f"Method: page_meta, name application: {context_page_meta['name_application']}")
            page = PageWidgets.objects.get(const_sys_property=cls.name_page)
            context_page_meta['title'] = page.title

            logger.debug(f"Method: page_meta, title: {context_page_meta['title']}")
            context_page_meta['header'] = page.header

            logger.debug(f"Method: page_meta, header: {context_page_meta['header']}")
            logger.debug('End HomePageMixin, method: page_meta')
            context_page_meta['name_page'] = cls.name_page
        except Exception as error:
            value = 'Unknown'
            context_page_meta['name_application'] = value
            context_page_meta['search_field_value'] = value
            context_page_meta['title'] = value
            context_page_meta['header'] = value
            context_page_meta['name_page'] = value
            logger.error(error)
        finally:
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

        if user.is_authenticated:
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


class WidgetsMixin:
    search_keywords = None
    http_user_agent = None
    browser = None
    page = None

    @classmethod
    def get_type_browser(cls, http_user_agent):
        for browser in TypeBrowser.objects.all():
            if browser.attribute in http_user_agent or browser.attribute == 'all':
                return browser
        return None

    @classmethod
    def request_meta(cls, request):
        cls.search_keywords = request.GET.get('search')
        logger.debug(f'Search keywords: {cls.search_keywords}')
        cls.http_user_agent = request.META['HTTP_USER_AGENT']
        logger.debug(f'http user-agent: {cls.http_user_agent}')
        cls.browser = cls.get_type_browser(cls.http_user_agent)
        logger.debug(f'check type browser: {cls.browser}')
        cls.page = PageWidgets.objects.get(const_sys_property=cls.name_page)
        logger.debug(f'attribute page: {cls.page.const_sys_property}')

    @classmethod
    def filter_widgets(cls, widgets_groups, search_keywords, browser):
        list_widgets = []
        for group in widgets_groups:
            if search_keywords is not None and len(search_keywords) > 0:
                logger.debug(f'Search keywords is not None')
                # widgets = list(LinkCards.objects.filter(is_active=True, widgets_groups=group, browser_type=browser,
                #                                         name__icontains=search_keywords).values())
                widgets = \
                    [card for card in
                     LinkWidgets.objects.filter(is_active=True, widgets_groups=group, browser_type=browser).values()
                     if search_keywords.lower() in card.get('name').lower()]

                logger.debug(f'Find link cards for group: {group}')

                # widgets.extend(
                #     MemoryCards.objects.filter(is_active=True, widgets_groups=group, browser_type=browser,
                #                                name__icontains=search_keywords).values()
                # )
                widgets.extend(
                    [card for card in
                     MemoryWidgets.objects.filter(is_active=True, widgets_groups=group, browser_type=browser).values()
                     if search_keywords.lower() in card.get('name').lower()]
                )
                logger.debug(f'Find memory cards for group: {group}')
            else:
                logger.debug(f'Search keywords is None')
                widgets = \
                    list(LinkWidgets.objects.filter(is_active=True, widgets_groups=group,
                                                    browser_type=browser).values())
                logger.debug(f'Find link cards for group: {group}')

                widgets.extend(list(MemoryWidgets.objects.filter(is_active=True, widgets_groups=group,
                                                                 browser_type=browser).values()))
                logger.debug(f'Find memory cards for group: {group}')

            if len(widgets) > 0:
                list_widgets.append({group.show_name: widgets})

        response = {'success': True, 'list_widgets': list_widgets}
        return response

    def get(self, request):
        """
        Данный миксин обслуживает запросы на получение виджетов пришедшие от зарегистрированных пользователей
        """
        try:
            self.request_meta(request)
            widgets_groups = WidgetsGroups.objects.filter(page=self.page)
            logger.debug(f'finding groups for page: {list(widgets_groups)}')
            logger.debug(f'Start filter cards for anon user')
            response = self.filter_widgets(widgets_groups, self.search_keywords, self.browser)
            logger.debug(f'response: {response}')
            return JsonResponse(response)
        except Exception as error:
            logger.error(error)
            response = {'success': False, 'message': str(error)}
            logger.debug(f'response: {response}')
            return JsonResponse(response)


class PrivateWidgetsMixin(WidgetsMixin):

    def get(self, request, **kwargs):
        """
        Данный миксин обслуживает запросы на получение виджетов пришедшие от зарегистрированных пользователей
        """
        try:
            logger.debug('Start method get in class PrivateCardsMixin')
            user = request.user
            logger.debug(f'username: {user.username}')
            if user.is_authenticated:
                logger.debug(f'User is authenticated')
                self.request_meta(request)
                user_groups = user.groups.all()
                logger.debug(f'user groups: {list(user_groups)}')
                widgets_groups = WidgetsGroups.objects.filter(page=self.page, access_group__in=user_groups)
                logger.debug(f'user card groups: {list(widgets_groups)}')
                response = self.filter_widgets(widgets_groups, self.search_keywords, self.browser)
                logger.debug(f'response: {response}')
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
