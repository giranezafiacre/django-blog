from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import datetime

class Post(models.Model):
    title = models.CharField(max_length=200,null=False)
    content = models.TextField(max_length=3000, help_text='Enter a content of the a post')
    image = models.ImageField(upload_to='uploads')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,verbose_name='created_by')
    created_on = models.DateField(default=datetime.date.today)
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

class Comment(models.Model):
    content = models.TextField(max_length=2000, help_text='Enter your comment')
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True,verbose_name='commented_on')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,verbose_name='commented_by')
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.content})'

class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True,verbose_name='Liked_on')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,verbose_name='commented_by')
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'