# Generated by Django 4.1.2 on 2022-11-06 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_auction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='owner',
        ),
        migrations.AddField(
            model_name='auction',
            name='owner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
