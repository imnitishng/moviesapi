from django.contrib import admin
from django.urls import path

from movies.urls import url_patterns as movie_endpoints


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += movie_endpoints
