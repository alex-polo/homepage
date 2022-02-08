import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from widgets.mixins import MemoryWidgetsMixin, PrivateWidgetsMixin, WidgetsMixin, HomePageMixin, BaseWidgetsMixin

logger = logging.getLogger('server')


@method_decorator(csrf_protect, name='dispatch')
class HomePageView(HomePageMixin, TemplateView):
    """Главная страница сайта для всех пользователей и анономных и зарегистрированных"""
    template_name = 'widgets/index.html'
    name_page = 'shared_page'


@method_decorator(csrf_protect, name='dispatch')
class UserProfilePageView(LoginRequiredMixin, HomePageView, TemplateView):
    """Страница сайта только для зарегистрированных пользователей"""
    template_name = 'widgets/index.html'
    name_page = 'private_page'


@method_decorator(csrf_protect, name='dispatch')
class SharedWidgetsPageView(WidgetsMixin, View):
    """Отдает список виджетов для главной страницы HomePageView"""
    name_page = 'shared_page'


@method_decorator(csrf_protect, name='dispatch')
class PrivateWidgetsPageView(LoginRequiredMixin, PrivateWidgetsMixin, View):
    """Отдает список виджетов для зарегистрированного пользователя"""
    name_page = 'private_page'
    login_url = 'login'


@method_decorator(csrf_protect, name='dispatch')
class MemoryWidgetsView(MemoryWidgetsMixin, View):
    """Отдает содержимое виджета памятки в соответствии с переданным id"""
    @classmethod
    def get(cls, request, pk):
        try:
            value = cls.response_context(request, pk)
            return JsonResponse({'success': True, 'value': value})
        except Exception as error:
            logger.error(error)
            return JsonResponse({'success': False, 'error': error})


# @method_decorator(csrf_protect, name='dispatch')
# class MediaLibraryView(LoginRequiredMixin, LibraryPageMixin, TemplateView):
#     template_name = 'homepage/library.html'
#     name_page = 'media_library_page'
#     login_url = 'login'


# @method_decorator(csrf_protect, name='dispatch')
# class TimeView(View):
#     http_method_names = ['get']
#
#     @classonlymethod
#     def json_context_data(self, request):
#         json_data = {'time': time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())}
#         return json_data
#
#     @classmethod
#     def get(cls, request):
#         json_response = cls.json_context_data(request)
#         return JsonResponse(json_response)
