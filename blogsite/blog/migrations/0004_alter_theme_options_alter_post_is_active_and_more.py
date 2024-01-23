# Generated by Django 4.2.1 on 2023-11-16 12:26

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_disliked_post_liked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='theme',
            options={'ordering': ['name'], 'verbose_name': 'Тема', 'verbose_name_plural': 'Теми'},
        ),
        migrations.AlterField(
            model_name='post',
            name='is_active',
            field=models.BooleanField(choices=[(False, 'Чернетка'), (True, 'Опублікований')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='post',
            name='theme',
            field=models.ForeignKey(default=blog.models.get_default_theme, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='theme', to='blog.theme', verbose_name='Тема'),
        ),
    ]