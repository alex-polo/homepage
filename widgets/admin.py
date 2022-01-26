from django.contrib import admin

from widgets.models import WidgetsGroups, PageWidgets, MemoryWidgets, LinkWidgets, TypeBrowser


@admin.register(PageWidgets)
class PageCardAdmin(admin.ModelAdmin):
    list_display = ('name_page',)
    list_display_links = ('name_page',)
    search_fields = ('name_page',)


@admin.register(WidgetsGroups)
class CardGroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'page_id', 'index_number', 'description', 'last_update_date')
    list_display_links = ('index_number', 'page_id', 'name', 'description')
    search_fields = ('name', 'page_id', 'index_number')


@admin.register(MemoryWidgets)
class MemoryCardAdmin(admin.ModelAdmin):
    list_display = ('index_number',
                    'name',
                    'is_active',
                    'last_update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    exclude = ('type',)


@admin.register(LinkWidgets)
class LinkCardsAdmin(admin.ModelAdmin):
    list_display = ('index_number',
                    'name',
                    'is_active',
                    'last_update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    exclude = ('type',)


@admin.register(TypeBrowser)
class TypeBrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'attribute', 'last_update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
