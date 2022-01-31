import logging

from hm_settings.models import HomepageSettings

logger = logging.getLogger('server')


class AccountDataMixin:
    template_name = None
    name_page = None

    def page_meta(self):
        return {
            'name_application': HomepageSettings.objects.get(property_attribute='name_application').property_value,
            'title': HomepageSettings.objects.get(property_attribute=f'title_{self.name_page}').property_value,
            'header': HomepageSettings.objects.get(property_attribute=f'header_{self.name_page}').property_value,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.page_meta())
        return context
    # template_name = None
    # name_page = None
    # name_application = None
    # title = None
    # header = None
    #
    # def page_meta(self):
    #     return {
    #         'name_application': self.name_application,
    #         'title': self.title,
    #         'header': self.header,
    #     }
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update(self.page_meta())
    #     return context
