import string
import random
from .models import Movie


def create_test_movie():
    test_movie = Movie(
        name = 'test_movie',
        desc = 'tests movie desc',
        dor = '1231-03-01'
    )
    test_movie.save()
    return test_movie.id.hex

def create_bulk_test_movies():
    for i in range(50):
        movie = Movie(
            name = get_random_string(10),
            desc = get_random_string(100),
            dor = '1999-03-01'
        )
        movie.save()

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
