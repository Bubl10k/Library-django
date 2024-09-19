from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import BookUser

from .models import Profile

@receiver(post_save, sender=BookUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(book_user=instance)


@receiver(post_save, sender=BookUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(book_user=instance)
    