from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from events.views import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("authentication.urls")),
    path('events/', include("events.urls")),
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
