from django.contrib import admin

from .models import Collection

# Register your models here.
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']
    list_filter = ['title']
    