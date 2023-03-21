import django_filters
from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    date_time = django_filters.DateTimeFilter(lookup_expr='lt', label='Datetime')
    
    class Meta:
        model = Post
        fields = ('date_time','title', 'author')