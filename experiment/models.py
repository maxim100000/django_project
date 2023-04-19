from django.contrib.auth.models import Group, User
from django.db import models
from django.urls import reverse


class Announcement(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=20)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('preview')
    
    def __str__(self):
        return self.title

class Category(models.Model):
    choices = (('Танк', 'Танк'), 
               ('Хил', 'Хил'),
               ('ДД', 'ДД'),
               ('Торговец', 'Торговец'),
               ('Гилдмастер', 'Гилдмастер'),
               ('Квестгивер', 'Квестгивер'),
               ('Кузнец', 'Кузнец'),
               ('Кожевник', 'Кожевник'),
               ('Зельевар', 'Зельевар'),
               ('Мастер заклинаний', 'Мастер заклинаний'))
    
    name = models.CharField(max_length=20, choices=choices)
    
    def __str__(self):
        return self.name

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('preview')