from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('widgets.urls')),
    path('account/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^.*$', RedirectView.as_view(url='/', permanent=False)),
]
