# Generated by Django 2.0.2 on 2018-09-13 23:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('terms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='usersFollowing',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
