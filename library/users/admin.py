from django.contrib import admin

from .models import Contact, Profile, ReadingStats

# Register your models here.
@admin.register(Profile)
class ProfileADmin(admin.ModelAdmin):
    list_display = ['book_user', 'firstname', 'bio', 'created', 'updated']
    list_filter = ['book_user', 'firstname']
    search_fields = ['firstname']
    prepopulated_fields = {"slug": ("firstname", "lastname")}


@admin.register(ReadingStats)
class ReadingStatsAdmin(admin.ModelAdmin):
    list_display = ['profile',]
    list_filter = ['profile']
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']
    list_filter = ['user_from', 'user_to']
    search_fields = ['user_from', 'user_to']
    