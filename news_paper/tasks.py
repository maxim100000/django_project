import datetime

from .models import Post
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string


def send():
    items = [Post.objects.get(id=i.pk) for i in Post.objects.all()
     if datetime.date.today().day - 7 <= i.date_time.day <= datetime.date.today().day]
    
    html_content = render_to_string('everyweek_mail.html', {'items': items})
    msg = EmailMultiAlternatives(
        subject=f'Подборка',
        from_email='zhma-kin@yandex.ru',
        to=['max1001@yandex.ru'],
        )
    
    msg.attach_alternative(html_content, "text/html")
    
    msg.send()