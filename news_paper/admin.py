from django.contrib import admin
from .models import Post, Author, Category, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time')
    
admin.site.register(Post, PostAdmin)
