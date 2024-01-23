from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('all_posts/', views.ShowAllPosts.as_view(), name='show_all_posts'),
    path('draft_posts/', views.ShowAllPosts.as_view(draft=True), name='show_draft_posts'),
    path('saved_posts/', views.ShowAllPosts.as_view(reacted="saved"), name='show_saved_posts'),
    path('liked_posts/', views.ShowAllPosts.as_view(reacted="liked"), name='show_liked_posts'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='show_post'),
    path('post/draft/<slug:post_slug>/', views.ShowPost.as_view(draft=True), name='show_draft_post'),
    path('posts_by_theme/<slug:theme_slug>/', views.ShowPostsByTheme.as_view(), name='show_posts_by_theme'),

    path('themes/', views.ShowThemes.as_view(), name='themes'),
    path('redact_theme/<slug:theme_slug>/', views.RedactTheme.as_view(), name='redact_theme'),
    path('create_theme/', views.CreateTheme.as_view(), name='create_theme'),
    path('delete_theme/<slug:theme_slug>/', views.DeleteTheme.as_view(), name='delete_theme'),

    path('create_post/', views.CreatePost.as_view(), name='create_post'),
    path('delete_post/<slug:post_slug>/', views.DeletePost.as_view(), name='delete_post'),
    path('post/<slug:post_slug>/redact/', views.RedactPost.as_view(), name='redact_post'),
    path('my_post/<slug:post_slug>/redact/', views.RedactMyPost.as_view(), name='redact_my_post'),

    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('save_post/<int:post_id>/', views.make_save_post, name='save_post'),

    path('api/posts/', views.PostsAPI.as_view(), name='posts_api'),
    path('api/draft_posts/', views.PostsAPI.as_view(draft=True), name='draft_posts_api'),
    path('api/liked_posts/', views.PostsAPI.as_view(reacted='liked'), name='liked_posts_api'),
    path('api/saved_posts/', views.PostsAPI.as_view(reacted='saved'), name='save_posts_api'),

    path('api/post/<int:post_id>/', views.PostAPI.as_view(), name='post_api'),
    path('api/draft_post/<int:post_id>/', views.PostAPI.as_view(draft=True), name='drraft_post_api'),
    path('api/posts/<slug:theme_slug>/', views.PostsByThemeAPI.as_view(), name='posts_by_theme_api'),

    path('api/themes/', views.ThemesAPI.as_view(), name='themes_api'),
    path('api/theme/<slug:theme_slug>/', views.ThemeAPI.as_view(), name='theme_api'),
]
