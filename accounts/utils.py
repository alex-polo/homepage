import logging

logger = logging.getLogger('server')


class AccountDataMixin:
    template_name = None
    name_page = None
    name_application = None
    title = None
    header = None

    def page_meta(self):
        return {
            'name_application': self.name_application,
            'title': self.title,
            'header': self.header,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.page_meta())
        return context
