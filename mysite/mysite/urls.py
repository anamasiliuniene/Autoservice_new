from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = ([
                   path('admin/', admin.site.urls),
                   path('', include('autoservice.urls')),
                   path('accounts/', include('django.contrib.auth.urls')),
                   path("logout/", auth_views.LogoutView.as_view(), name="logout"),
                   path('tinymce/', include('tinymce.urls')),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
