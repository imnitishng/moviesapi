from django.contrib import admin
from django.urls import path

from .views import create_movie


url_patterns = [
    path(r'api/movies/add', create_movie, name='add_movie')
]
