# Generated by Django 4.2 on 2023-04-18 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]