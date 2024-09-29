from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import ReadingStats

from .models import BookUser


@receiver(post_save, sender=BookUser)
def update_reading_stats(sender, instance, created, **kwargs):
    '''
    Update reading stats when reading pages are added to a book
    '''
    if not created:
        now = datetime.now()
        month = now.month
        year = now.year
        profile = instance.profile
        
        reading_stats, _ = ReadingStats.objects.get_or_create(
            profile=profile,
            year=year,
            month=month,
            defaults={'pages_read': 0}
        )
        
        reading_stats.pages_read = instance.pages_read
        reading_stats.save()
        