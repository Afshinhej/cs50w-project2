# Generated by Django 4.1.2 on 2022-11-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
