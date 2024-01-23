from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('registration/', views.RegistrateUser.as_view(), name='registration'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:profile_pk>/', views.ShowProfile.as_view(), name='profile'),
    path('redact_profile/', views.RedactProfile.as_view(), name='redact_profile'),
    path('subscribe/<int:user_id>/', views.subscribe, name='subscribe'),
    path('subscribes/', views.ShowSubscribes.as_view(), name='show_subscribes'),
]
