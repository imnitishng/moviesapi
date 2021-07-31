from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import movies_list, movie_details


url_patterns = [
    path(r'api/movies', movies_list, name='movies_list'),
    path(r'api/movies/<str:id>', movie_details, name='movie_details'),
]
