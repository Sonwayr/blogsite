from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, F
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from blog.models import Post
from users.forms import RegistrateUserForm, LoginUserForm, RedactProfileForm


# Create your views here.
class RegistrateUser(CreateView):
    form_class = RegistrateUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Реєстрація', 'btn_name': 'Зареєструватись'}


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/registration.html'
    extra_context = {'title': 'Авторизація', 'btn_name': 'Авторизуватись'}


class ShowProfile(LoginRequiredMixin, DetailView):
    model = get_user_model()  # User
    template_name = 'users/profile.html'
    pk_url_kwarg = 'profile_pk'
    context_object_name = 'profile'
    extra_context = {'title': 'Профіль'}
    paginate_by = 10  # Устанавливает количество постов на странице

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs.get('profile_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.active.select_related('theme', 'author').filter(author=self.kwargs.get('profile_pk'))

        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['page_obj'] = paginator.get_page(page)
        context['posts'] = posts
        return context


class RedactProfile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = RedactProfileForm
    template_name = 'blog/create_theme.html'
    extra_context = {'title': 'Редагування профілю', 'btn_name': 'Зберегти'}

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'profile_pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def subscribe(request, user_id):
    user = request.user
    user_to_subscribe = get_object_or_404(get_user_model(), pk=user_id)
    if user_to_subscribe != user:
        if not user.subscribes.filter(pk=user_to_subscribe.pk).exists():
            user.subscribes.add(user_to_subscribe)
            user_to_subscribe.subscribers = F('subscribers') + 1
        else:
            user.subscribes.remove(user_to_subscribe)
            user_to_subscribe.subscribers = F('subscribers') - 1
        user.save()
        user_to_subscribe.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


class ShowSubscribes(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users/subscribes.html'
    context_object_name = 'subscribes'
    paginate_by = 10
    extra_context = {'title': 'Підписки'}

    def get_queryset(self):
        return self.request.user.subscribes.all()
