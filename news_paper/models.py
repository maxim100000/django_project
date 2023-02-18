import functools

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(help_text='Рейтинг пользователя')

    def update_rating(self):
        overall_article_rating = sum([x['rating'] for x in self.post_set.values('rating')]) * 3 
        overall_comments_rating = sum(functools.reduce(lambda x, y: x + y, [[i['rating'] for i in x.comment_set.values('rating')]
                                                                            for x in self.post_set.filter()]))
        overall_comment_to_articles_rating = sum([x.rating for x in self.post_set.filter()]) 
        self.rating = overall_comment_to_articles_rating + overall_comments_rating + overall_article_rating
        
class Category(models.Model):
    name = models.CharField(max_length=20, help_text='Категория новостей/статей', unique=True)


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
