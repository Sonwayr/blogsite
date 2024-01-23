from django.contrib.auth import get_user_model
from django.db import models
import transliterate
from django.urls import reverse
from django.utils.text import slugify

from blogsite.settings import DEFAULT_THEME_SLUG


class ActivePostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Post.Status.ACTIVE)


class DraftPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Post.Status.DRAFT)


class Theme(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Назва теми')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Теми'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_posts_by_theme', kwargs={'theme_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = transliterate.slugify(self.name)
        super().save(*args, **kwargs)


def get_default_theme():
    return Theme.objects.get(slug=DEFAULT_THEME_SLUG)


# Create your models here.
class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Чернетка'
        ACTIVE = 1, 'Опублікований'

    title = models.CharField(max_length=255, verbose_name='Назва', unique=True)

    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='Слаг')

    content = models.TextField(verbose_name='Зміст поста')

    photo = models.ImageField(upload_to='photos/%Y/%m/%d', default=None, blank=True,
                              null=True, verbose_name='Фото')

    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Час створення')

    theme = models.ForeignKey('Theme', on_delete=models.SET_DEFAULT, default=get_default_theme,
                              related_name='theme', verbose_name='Тема')

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True,
                               related_name='Власник')

    is_active = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                    default=Status.DRAFT, verbose_name='Статус')

    liked = models.IntegerField(default=0, blank=True, verbose_name='Кількість лайків')
    disliked = models.IntegerField(default=0, blank=True, verbose_name='Кількість дизлайків')
    saved = models.IntegerField(default=0, blank=True, verbose_name='Кількість збережень')

    objects = models.Manager()
    active = ActivePostManager()
    draft = DraftPostManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['time_create']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
