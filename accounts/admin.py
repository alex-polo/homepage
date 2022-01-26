from django.contrib import admin

from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from accounts.models import ApplicationUser, ApplicationUsersGroup

admin.site.unregister(Group)


@admin.register(ApplicationUsersGroup)
class CustomGroupAdmin(GroupAdmin):
    search_fields = ('name',)
    exclude = ('permissions',)


@admin.register(ApplicationUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'family_name')
    list_filter = ('is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'family_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser', 'groups'),
        }),
    )
