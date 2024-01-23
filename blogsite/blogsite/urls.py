from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blogsite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('users/', include('users.urls', namespace='users')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Адмін панель"
admin.site.index_title = "Sonwayr`s blog"
