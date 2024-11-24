from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin
from products.views import IndexView, ContactView

from django.urls import include, path, re_path

static_urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('check-task-status/', IndexView.as_view(), name='check_task_status'),
    path('translater/', include('products.urls', namespace='translater')),
    path('contact/', ContactView.as_view(), name='contact'),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.TESTING:
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
