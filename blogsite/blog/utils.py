from django.db.models import Q
from django.http import Http404

from blog.models import Post


class BasePostMixin:
    reacted = None
    draft = False


class DataMixin:

    def get_search(self, request):
        return request.GET.get('search')

    def get_mixin_context(self, context, search, **kwargs):
        if search:
            context['search'] = search
            if context.get('posts_type', ''):
                context['posts_type'] += f' які містять {search}'
            else:
                context['posts_type'] = f'Пости які містять {search}'
        context.update(**kwargs)
        return context


class AllPostMixin(BasePostMixin):

    def posts_queryset(self, request):
        match self.reacted:
            case 'liked':
                queryset = request.user.liked_post.all()
                return queryset

            case 'saved':
                queryset = request.user.saved_post.all()
                return queryset
        if self.draft:
            queryset = Post.draft.all().select_related('theme', 'author')
        else:
            queryset = Post.active.all().select_related('theme', 'author')
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(theme__name__icontains=search))

        return queryset


class ByThemeMixin:
    def posts_by_theme(self, kwargs, request):
        theme_slug = kwargs.get('theme_slug')
        search = request.GET.get('search')
        if search:
            return Post.active.select_related('theme', 'author').filter(
                Q(theme__slug=theme_slug) & Q(title__icontains=search))
        return Post.active.select_related('theme', 'author').filter(theme__slug=theme_slug)


class DetailPostMixin(BasePostMixin):
    def check_permission(self, request):
        if not self.draft:
            return Post.active.select_related('author', 'theme')
        else:
            if not request.user.has_perm('blog.change_post'):
                raise Http404("У вас немає прав переглядати чернетки.")
            return Post.draft.select_related('author', 'theme')
