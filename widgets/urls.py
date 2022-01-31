from django.urls import path

from widgets.views import HomePageView, UserProfilePageView, SharedWidgetsPageView, \
    PrivateWidgetsPageView, MemoryWidgetsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/shared-widgets/', SharedWidgetsPageView.as_view(), name='shared-widgets'),
    path('user-profile/<slug:slug>/', UserProfilePageView.as_view(), name='user-profile'),
    path('user-profile/<slug:slug>/widgets/', PrivateWidgetsPageView.as_view(), name='private-widgets'),
    path('memory-widgets/<int:pk>', MemoryWidgetsView.as_view(), name='memory-widgets'),

    # path('library/<slug:slug>', MediaLibraryView.as_view(), name='library'),
    # path('home/private-cards', PrivateCardsPageView.as_view(), name='private-cards'),
    # path('home/time/', TimeView.as_view(), name='home-time'),
    # path('user-cards/<slug:slug>', UserHomePageView.as_view(), name='user-cards'),
]
