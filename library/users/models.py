from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    book_user = models.OneToOneField('books.BookUser', 
                                     on_delete=models.CASCADE, 
                                     related_name='profile')
    image = models.ImageField(upload_to='users', 
                              null=True, 
                              blank=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, 
                                  blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=False)
    
    class Meta:
        ordering = ['firstname']
        indexes = [
            models.Index(fields=['lastname']),
        ]
    
    def __str__(self) -> str:
        return self.firstname + ' ' + self.lastname
    
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={"pk": self.pk})
    

class ReadingStats(models.Model):
    profile = models.ForeignKey(Profile, 
                                   on_delete=models.CASCADE, 
                                   related_name='reading_stats')
    year = models.IntegerField()
    month = models.IntegerField()
    pages_read = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Reading Stats'
        unique_together = ['profile', 'year', 'month']
        ordering = ['year', 'month']
        
    def __str__(self):
        return f"{self.profile.book_user.user.username} - {self.year}/{self.month}"


class Contact(models.Model):
    user_from = models.ForeignKey('books.BookUser', 
                                  on_delete=models.CASCADE,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey('books.BookUser',
                                on_delete=models.CASCADE,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
        
    def __str__(self) -> str:
        return f'{self.user_from} follows {self.user_to}'
