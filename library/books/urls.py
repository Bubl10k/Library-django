from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html'), name='logout'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change.html'),
         name='password_change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
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
