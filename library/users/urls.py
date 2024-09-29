from django.conf.urls import include
from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    # auth urls
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
     
    # profile urls
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/following/', views.profile_list, 
         name='profile_list_following', kwargs={'follow': True}),
    path('profile/<int:pk>', cache_page(60*15)(views.profile_detail), name='profile_detail'),
    path('profile/<int:pk>/other', cache_page(60*15)(views.profile_detail), name='profile_detail_other', 
         kwargs={'other': True}),
    path('follow/', views.user_follow, name='user_follow'),
    path('profile_edit/<int:pk>/', views.profile_edit, name='profile_edit'),
    path('get_favorites/<int:pk>/', views.get_favorites, name='get_favorites'),
    path('api/reading-stats/<int:pk>', views.reading_stats,
         name='reading_stats_api'),
]
