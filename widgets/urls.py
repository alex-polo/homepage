from django.urls import path

from widgets.views import HomePageView, UserProfilePageView, MediaLibraryView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/user-profile/<slug:slug>/', UserProfilePageView.as_view(), name='user-profile'),
    # path('memory-cards/<int:pk>', MemoryCardsView.as_view(), name='memory-cards'),
    # path('home/shared-widgets/', SharedCardsPageView.as_view(), name='shared-cards'),
    # path('home/user-profile/<slug:slug>/widgets/', PrivateCardsPageView.as_view(), name='private-cards'),
    path('library/<slug:slug>', MediaLibraryView.as_view(), name='library'),
    # path('home/private-cards', PrivateCardsPageView.as_view(), name='private-cards'),
    # path('home/time/', TimeView.as_view(), name='home-time'),
    # path('user-cards/<slug:slug>', UserHomePageView.as_view(), name='user-cards'),
]
