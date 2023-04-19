import datetime

from .models import Announcement
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send():
    items = [Announcement.objects.get(id=i.pk) for i in Announcement.objects.all()
             if datetime.date.today().day - 7 <= i.date_time.day <= datetime.date.today().day]

    html_content = render_to_string('everyweek_mail.html', {'items': items})
    msg = EmailMultiAlternatives(
        subject=f'Подборка',
        from_email='',
        to=[''],
    )

    msg.attach_alternative(html_content, "text/html")

    msg.send()
