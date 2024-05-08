from django.urls import include, path, re_path
from django.contrib import admin
from rest_framework import routers
from django.shortcuts import redirect
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('', lambda req: redirect('login/')),
    path('', include('authentication.urls')),
    path('api/plantation/', include('plantation.urls')),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)