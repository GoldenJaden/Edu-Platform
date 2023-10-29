import os
from django.contrib import admin
from django.urls import path, include

django_nginx = os.environ.get("DJANGO_NGINX_PREFIX")

urlpatterns = [
    path(django_nginx + 'admin/', admin.site.urls),
    path(django_nginx + 'api/user/', include("User.urls")),
    path(django_nginx + 'api/edu/', include("Edu.urls")),

]

