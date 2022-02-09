from django.contrib import admin

from widgets.models import WidgetsGroups, MemoryWidgets, LinkWidgets, TypeBrowser


@admin.register(WidgetsGroups)
class WidgetsGroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'page', 'index_number', 'description', 'last_update_date')
    list_display_links = ('index_number', 'page', 'name', 'description')
    list_filter = ('page',)
    search_fields = ('name', 'page', 'index_number')


@admin.register(MemoryWidgets)
class MemoryWidgetsAdmin(admin.ModelAdmin):
    list_display = ('is_active',
                    'name',
                    'content',
                    'index_number',
                    'last_update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'widgets_groups',)
    exclude = ('type',)


@admin.register(LinkWidgets)
class LinkWidgetsAdmin(admin.ModelAdmin):
    list_display = ('is_active',
                    'name',
                    'url',
                    'index_number',
                    'last_update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'widgets_groups',)
    exclude = ('type',)


@admin.register(TypeBrowser)
class TypeBrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'attribute', 'last_update_date')
    list_display_links = ('name',)
    search_fields = ('name',)
