# Generated by Django 4.2.1 on 2023-11-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_theme_options_alter_post_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='saved',
            field=models.IntegerField(blank=True, default=0, verbose_name='Кількість збережень'),
        ),
    ]
