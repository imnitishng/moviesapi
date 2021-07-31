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
    test_movie = Movie(
        name = 'test_movie',
        desc = 'tests movie desc',
        dor = '1231-03-01'
    )
    test_movie.save()
