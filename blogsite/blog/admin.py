from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'content', 'show_photo',
                    'time_create', 'theme', 'liked', 'disliked', 'saved', 'is_active']
    list_display_links = ['slug']
    list_editable = ['is_active']
    list_per_page = 10
    search_fields = ['title']
    list_filter = ['theme', 'is_active', 'time_create']
    actions = ['set_active', 'set_inactive']

    @admin.display(description='Фото')
    def show_photo(self, post: Post):
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' width=50>")
        return 'Без фото'

    @admin.action(description='Активувати обрані пости')
    def set_active(self, request, queryset):
        count = queryset.update(is_active=Post.Status.ACTIVE)
        return self.message_user(request, f'Було активовано {count} постів')

    @admin.action(description="Деактивувати обрані пости")
    def set_inactive(self, request, queryset):
        count = queryset.update(is_active=Post.Status.DRAFT)
        return self.message_user(request, f'Було деактивовано {count} постів')


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_display_links = ['slug']
    list_per_page = 10
    search_fields = ['name']
    list_editable = ['name']
