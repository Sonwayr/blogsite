# Generated by Django 4.2.1 on 2023-11-17 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_disliked_post_alter_user_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscribers',
        ),
        migrations.AddField(
            model_name='user',
            name='subscribers',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL, verbose_name='Підписники'),
        ),
    ]