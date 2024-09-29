from django.urls import path

from . import views


urlpatterns = [
    path('', views.book_list, 
         name='book_list'),
    path('create/', views.create_book, 
         name='create_book'),
    path('delete/<int:pk>', views.delete_book, 
         name='delete_book'),
    path('change_status/<int:pk>', views.change_status, 
         name='change_status'),
    path('update/<int:pk>', views.update_book, 
         name='update_book'),
    path('favorite/<int:pk>', views.book_favorite, 
         name='book_favorite'),
    path('add_book_collection/<int:pk>', views.add_book_from_collection,
         name='add_book_collection'),
]
