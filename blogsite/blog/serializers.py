from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Post, Theme


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields()
        # Например, сделаем field1 только для чтения в зависимости от какого-то условия
        if self.context['request'].method in ['PUT', 'PATCH']:
            read_only_fields = ['slug', 'time_create', 'author', 'liked', 'disliked', 'saved']
        else:
            read_only_fields = ['slug', 'time_create', 'author', 'is_active', 'liked', 'disliked', 'saved']
        for field_name in read_only_fields:
            fields[field_name].read_only = True

        return fields


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = '__all__'
        read_only_fields = ['slug']
