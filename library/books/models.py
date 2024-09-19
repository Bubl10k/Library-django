from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Contact

# Create your models here.
class BookUser(models.Model):
    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE)
    current_page = models.IntegerField(default=0)
    pages_read = models.IntegerField(verbose_name='The number of pages read', 
                                     default=0)
    books_read = models.ManyToManyField('Book',
                                          related_name='readers',
                                          blank=True)
    following = models.ManyToManyField('self',
                                       through=Contact,
                                       related_name='followers',
                                       symmetrical=False)
    objects = models.Manager()
    
    def __str__(self) -> str:
        return f'Book user: {self.user.username}'
    
    @receiver(post_save, sender=User)
    def create_book_user(sender, instance, created, **kwargs):
        if created:
            BookUser.objects.create(user=instance)
            
    
    @receiver(post_save, sender=User)
    def save_book_user(sender, instance, **kwargs):
        instance.bookuser.save()
        
    def get_all_books(self):
        return self.books.count()
    
    
class Book(models.Model):
    class Status(models.TextChoices):
        READ = 'R', 'Read'
        UNREAD = 'U', 'Unread'
    
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, 
                              default='Unknown')
    num_pages = models.IntegerField(verbose_name='Amount of pages')
    cur_num_pages = models.IntegerField(verbose_name='Current page',
                                        default=0)
    description = models.TextField(blank=True,
                                   null=True)
    objects = models.Manager()
    user = models.ManyToManyField(to=BookUser,
                                  related_name='books')
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, 
                              choices=Status.choices, 
                              default=Status.UNREAD)
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['start_date',]),
        ]
        ordering = ['is_favorite', '-start_date']
    
    def __str__(self) -> str:
        return self.title
