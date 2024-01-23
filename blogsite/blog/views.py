from django.utils.text import slugify
from rest_framework import generics
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q, F
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .forms import CreateThemeForm, CreatePostForm, RedactPostForm, RedactThemeForm
from .models import *
from .permissions import CanRedactThemeOrReadOnly, CanRedactPostOrReadOnly
from .utils import DataMixin, AllPostMixin, DetailPostMixin, ByThemeMixin
from .serializers import PostSerializer, ThemeSerializer


# Create your views here.
class MainPage(TemplateView):
    template_name = 'blog/main_page.html'
    extra_context = {'title': 'Головна сторінка', 'info': 'Блог сайт'}


class ShowAllPosts(AllPostMixin, DataMixin, ListView):
    model = Post
    template_name = 'blog/show_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return self.posts_queryset(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.get_search(self.request)
        if self.draft:
            context['title'] = 'Чернетки'
            context['posts_type'] = 'Чернетки'
            context['draft'] = self.draft
        elif self.reacted == 'saved':
            context['title'] = 'Збережені'
            context['posts_type'] = 'Збережені'
        elif self.reacted == 'liked':
            context['title'] = 'Лайкнуті'
            context['posts_type'] = 'Лайкнуті'
        else:
            if not search:
                context['posts_type'] = 'Пости на сайті'
                context['title'] = 'Усі пости'
            elif search:
                context['search'] = search
                context['title'] = 'Пости за пошуком' + search

        return self.get_mixin_context(context, search=search)


class ShowPost(LoginRequiredMixin, DetailPostMixin, DetailView):
    model = Post
    template_name = 'blog/show_post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_queryset(self):
        return self.check_permission(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Відображення поста ' + context['post'].title
        return context

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get(self.slug_url_kwarg))


class ShowPostsByTheme(ByThemeMixin, DataMixin, ListView):
    model = Post
    template_name = 'blog/show_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.posts_by_theme(self.kwargs, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.get_search(self.request)
        theme_slug = self.kwargs.get('theme_slug')
        theme = get_object_or_404(Theme, slug=theme_slug)
        context['title'] = f'Тема - {theme.name}'
        context['posts_type'] = f'Пости за темою {theme.name}'
        return self.get_mixin_context(context, search)


class ShowThemes(ListView):
    model = Theme
    template_name = 'blog/show_categories.html'
    paginate_by = 52
    context_object_name = 'themes'
    extra_context = {'title': 'Теми на сайті'}


class CreateTheme(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'blog/create_theme.html'
    form_class = CreateThemeForm
    success_url = reverse_lazy('show_all_posts')
    extra_context = {'title': 'Створення теми', 'btn_name': 'Створити'}
    permission_required = 'blog.add_theme'

    def form_valid(self, form):
        theme = form.save()
        return super().form_valid(form)


class CreatePost(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'blog/create_theme.html'
    form_class = CreatePostForm
    extra_context = {'title': 'Створення поста', 'btn_name': 'Створити'}
    success_url = reverse_lazy('show_all_posts')
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class RedactPost(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = RedactPostForm
    slug_url_kwarg = 'post_slug'
    template_name = 'blog/create_theme.html'
    extra_context = {'title': "Редагування поста", 'btn_name': 'Зберегти'}
    permission_required = 'blog.change_post'
    success_url = reverse_lazy('show_all_posts')


class DeletePost(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('show_all_posts')
    permission_required = 'blog.delete_post'
    extra_context = {'title': 'Видалення', 'btn_name': 'Видалити'}
    template_name = 'blog/confirm_delete.html'


class RedactTheme(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Theme
    slug_url_kwarg = 'theme_slug'
    form_class = RedactThemeForm
    permission_required = 'blog.change_theme'
    template_name = 'blog/create_theme.html'
    extra_context = {'title': 'Редагування теми', 'btn_name': 'Зберегти'}


class DeleteTheme(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Theme
    slug_url_kwarg = 'theme_slug'
    success_url = reverse_lazy('themes')
    permission_required = 'blog.delete_theme'
    extra_context = {'title': 'Видалення', 'btn_name': 'Видалити'}
    template_name = 'blog/confirm_delete.html'


@login_required
def like_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    if post_id in user.liked_post.values_list('id', flat=True):
        user.liked_post.remove(post)
        post.liked = F('liked') - 1

    elif post_id in user.disliked_post.values_list('id', flat=True):
        user.disliked_post.remove(post)
        post.disliked = F('disliked') - 1
        user.liked_post.add(post)
        post.liked = F('liked') + 1

    else:
        user.liked_post.add(post)
        post.liked = F('liked') + 1

    user.save()
    post.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def dislike_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    if post_id in user.disliked_post.values_list('id', flat=True):
        user.disliked_post.remove(post)
        post.disliked = F('disliked') - 1

    elif post_id in user.liked_post.values_list('id', flat=True):
        user.liked_post.remove(post)
        post.liked = F('liked') - 1
        user.disliked_post.add(post)
        post.disliked = F('disliked') + 1

    else:
        user.disliked_post.add(post)
        post.disliked = F('disliked') + 1

    user.save()
    post.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def make_save_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    if post_id in user.saved_post.values_list('id', flat=True):
        user.saved_post.remove(post)
        post.saved = F('saved') - 1
    else:
        user.saved_post.add(post)
        post.saved = F('saved') + 1

    user.save()
    post.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


class RedactMyPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = RedactPostForm
    slug_url_kwarg = 'post_slug'
    template_name = 'blog/create_theme.html'
    extra_context = {'title': 'Редагування поста', 'btn_name': 'Зберегти'}

    def test_func(self):
        post = get_object_or_404(Post, slug=self.kwargs.get('post_slug'))
        return self.request.user.is_authenticated and self.request.user == post.author


class PostsAPI(AllPostMixin, generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = self.posts_queryset(self.request)
        return queryset

    def perform_create(self, serializer):
        title = serializer.validated_data['title']

        slug = transliterate.slugify(title)
        serializer.save(author=self.request.user, slug=slug)


class PostAPI(DetailPostMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'
    permission_classes = (CanRedactPostOrReadOnly,)

    def get_queryset(self):
        return self.check_permission(self.request)

    def perform_update(self, serializer):
        title = serializer.validated_data['title']

        slug = transliterate.slugify(title)
        serializer.save(slug=slug)


class PostsByThemeAPI(ByThemeMixin, generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.posts_by_theme(self.kwargs, self.request)


class ThemesAPI(generics.ListCreateAPIView):
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()
    permission_classes = (CanRedactThemeOrReadOnly,)


class ThemeAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ThemeSerializer
    lookup_url_kwarg = 'theme_slug'
    lookup_field = 'slug'
    queryset = Theme.objects.all()
    permission_classes = (CanRedactThemeOrReadOnly,)

    def perform_update(self, serializer):
        name = serializer.validated_data.get('name')
        slug = transliterate.slugify(name)
        serializer.save(slug=slug)
