from django.contrib.auth.models import User
from django.db import models

from books.models import Book

# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=40)
    books = models.ManyToManyField(Book, 
                                   related_name='collections',
                                   blank=True)
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE, 
                             related_name='collections')
    objects = models.Manager()
    
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'user']
    
    def __str__(self) -> str:
        return self.title
    