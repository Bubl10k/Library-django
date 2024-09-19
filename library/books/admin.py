from django.contrib import admin

from .models import BookUser, Book

# Register your models here.
@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'num_pages', 'cur_num_pages', 'status']
    list_filter = ['status', 'start_date', 'is_favorite']
    date_hierarchy = 'start_date'
    ordering = ['start_date']
    

@admin.register(BookUser)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_page', 'pages_read']
