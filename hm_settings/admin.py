from django.contrib import admin

from hm_settings.models import HomepageSettings

admin.site.site_header = 'Homepage, администрирование'


@admin.register(HomepageSettings)
class MainConstProperty(admin.ModelAdmin):
    list_display = ('property', 'property_value')
    list_display_links = ('property', 'property_value')
    search_fields = ('property', 'property_value')
