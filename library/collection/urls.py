from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    path('', cache_page(60*15)(views.collection_list), name='collection_list'),
    path('search_books/', views.search_books, name='search_books'),
    path('delete_book_from_collection/<collection_pk>/<book_pk>/',
         views.delete_book_from_collection, name='delete_book_from_collection'),
    path('add_book/<int:pk>/', views.add_book, name='add_book'),
    path('add_collection/', views.add_collection, name='add_collection'),
    path('get_books/<int:pk>/', views.get_books_from_collection, name='get_books'),
    path('delete_collection/<int:pk>',
         views.delete_collection, name='delete_collection'),
    path('update_collection/<int:pk>',
         views.update_collection, name='update_collection'),
]
