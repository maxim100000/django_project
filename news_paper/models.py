import functools

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserCreationForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.utils.timezone import now


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(help_text='Рейтинг пользователя')
    
    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        overall_article_rating = sum([x['rating'] for x in self.post_set.values('rating')]) * 3 
        overall_comments_rating = sum(functools.reduce(lambda x, y: x + y, [[i['rating'] for i in x.comment_set.values('rating')]
                                                                            for x in self.post_set.filter()]))
        overall_comment_to_articles_rating = sum([x.rating for x in self.post_set.filter()]) 
        self.rating = overall_comment_to_articles_rating + overall_comments_rating + overall_article_rating
        
        
class Category(models.Model):
    name = models.CharField(max_length=20, help_text='Категория новостей/статей', unique=True)
    subscribers = models.ManyToManyField(User)
    
    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    record = models.CharField(max_length=20, help_text='Публикация', choices=[('A', 'article'), ('N', 'news')])
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=100, help_text='Заголовок статьи/новости')
    text = models.TextField(help_text='Текст статьи/новости')
    rating = models.PositiveSmallIntegerField()
    
    def like(self):
        self.rating += 1
        self.save()
        
        
    def dislike(self):
        self.rating -= 1
        self.save()
        
    def preview(self):
        return self.text[:125] + '...'
        

    def __str__(self):
        return f'{self.title} {self.preview()}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(help_text='Текст комментария')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время', help_text='Дата и время создания') 
    rating = models.PositiveSmallIntegerField()
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()

class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class BasicSignForm(SignupForm):
    def save(self, request):
        user = super(BasicSignForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class Appointment(models.Model):
    date = models.DateField(default=now())
    client_name = models.CharField(max_length=200)
    message = models.TextField()
    
    def __str__(self):
        return f'{self.client_name}: {self.message}'