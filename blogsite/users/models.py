from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', verbose_name='Фото', blank=True, null=True)
    date_birth = models.DateTimeField(blank=True, null=True,
                                      verbose_name='Дата народження')

    subscribes = models.ManyToManyField('self', blank=True, symmetrical=False,
                                        default=None, verbose_name='Підписки')

    subscribers = models.IntegerField(blank=True, default=0, verbose_name='Підписники')

    liked_post = models.ManyToManyField('blog.Post', blank=True, default=None,
                                        related_name='liked_post', verbose_name='Лайкнуті')
    disliked_post = models.ManyToManyField('blog.Post', blank=True, default=None,
                                           related_name='disliked_post', verbose_name='Дізлайкнуті')
    saved_post = models.ManyToManyField('blog.Post', blank=True, default=None,
                                        related_name='saved_post', verbose_name='Збережені')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.username})"
