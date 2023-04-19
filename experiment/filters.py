import django_filters
from django_filters import FilterSet
from .models import Announcement


class AnnouncementFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='По объявлению')
    

    class Meta:
        model = Announcement
        fields = ('title',)
