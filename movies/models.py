import uuid
from django.db import models


class Movie(models.Model):
    """
    The Movie model represents all the metadata for
    a movie.

    Attributes:
        id: UUID Primary Key, unique for every movie
        name: Movie name
        desc: Movie description
        dor: Date of release for the movie
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    dor = models.DateField()