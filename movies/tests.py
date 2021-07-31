from movies.models import Movie
from django.test import TestCase, client
from rest_framework.test import APIClient

from .test_utils import create_test_movie, create_bulk_test_movies


class TestMoviesPOST(TestCase):
    '''
    Test POST operations for movies
    '''
    url = '/api/movies'

    def test_create_movie_complete_request(self):
        '''
        Movie object is created and returned with proper status code 201
        when complete data is provided in the request.
        '''
        client = APIClient()
        payload = {
            "name": "test movie",
            "desc": "test movie description",
            "dor": "1999-01-01"
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], 'test movie')
        self.assertEqual(response.data['desc'], 'test movie description')
        self.assertEqual(response.data['dor'], '1999-01-01')

    def test_create_movie_incomplete_request(self):
        '''
        Test 400 BAD_REQUEST with error details is raised when incomplete data 
        is provided as request.
        '''
        client = APIClient()
        payload = {
            "desc": "test movie description",
            "dor": "1999-01-01"
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'This field is required.', status_code=400)
        self.assertIn('name', response.data)

    def test_create_movie_with_invalid_date_format(self):
        client = APIClient()
        payload = {
            "name": "test movie",
            "desc": "test movie description",
            "dor": "01-01-1999"
        }
        response = client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.', status_code=400)


class TestMoviesPUT(TestCase):
    '''
    Test PUT operations for movies
    '''
    @classmethod
    def setUpTestData(cls):
        '''
        Save a movie entry before running the tests to edit it 
        inside the tests using API requests
        '''
        cls.movie_id = create_test_movie()

    def test_edit_movie_complete_request(self):
        '''
        Test update a movie information for the ID specified as URL param
        and data specified as JSON request data to the endpoint.
        '''
        client = APIClient()
        payload = {
            "name": "test movie nitish",
            "desc": "test movie description nitish",
            "dor": "1999-01-01"
        }
        url = f'/api/movies/{self.movie_id}'

        response = client.put(url, payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data['id'], self.movie_id)
        self.assertEqual(response.data['name'], 'test movie nitish')
        self.assertEqual(response.data['desc'], 'test movie description nitish')
        self.assertEqual(response.data['dor'], '1999-01-01')

    def test_edit_movie_with_invalid_id(self):
        '''
        Test proper 404 raised when invalid request ID is specified as
        URL paramaeter
        '''
        client = APIClient()
        payload = {
            "name": "test movie nitish",
            "desc": "test movie description nitish",
            "dor": "1999-01-01"
        }
        url = f'/api/movies/invalid_request_id'

        response = client.put(url, payload, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Movie ID not found', status_code=404)


class TestMoviesGET(TestCase):
    '''
    Test GET operations for movies
    '''
    @classmethod
    def setUpTestData(cls):
        '''
        Save bulk movie entries before running the tests to GET info
        '''
        create_bulk_test_movies()
        cls.movie_id = Movie.objects.all()[0].id.hex

    def test_get_all_movies(self):
        '''
        Test getting all movies first page, the URL for previous page should be
        absent and URL for the next page should be present.
        '''
        client = APIClient()
        url = f'/api/movies'
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 20)
        self.assertIsNone(response.data['previous'])
        self.assertIsNotNone(response.data['next'])

    def test_get_movies_paginated_content(self):
        '''
        Test getting all movies paginated content for page 2 where previous and
        next pages should be present
        '''
        client = APIClient()
        url = f'/api/movies?page=2'
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 20)
        self.assertIsNotNone(response.data['previous'])
        self.assertIsNotNone(response.data['next'])

    def test_get_movies_paginated_content_final_page(self):
        '''
        Test getting all movies paginated content for last page where previous only
        previous content is present
        '''
        client = APIClient()
        url = f'/api/movies?page=3'
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['previous'])
        self.assertIsNone(response.data['next'])


    def test_get_movie_from_valid_id(self):
        '''
        Test getting a movie from ID passed in the URL returns a single movie instance
        '''
        client = APIClient()
        url = f'/api/movies/{self.movie_id}'
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.movie_id)
        self.assertIn('name', response.data)
        self.assertIn('desc', response.data)
        self.assertIn('dor', response.data)
        self.assertNotIn('next', response.data)
        self.assertNotIn('previous', response.data)


    def test_get_movie_from_invalid_id(self):
        '''
        Test getting a movie from invalid ID passed in the URL returns 404 not found
        '''
        client = APIClient()
        url = f'/api/movies/invalid_movie_id'
        response = client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Movie ID not found', status_code=404)


class TestMoviesDELETE(TestCase):
    '''
    Test DELETE operations for movies    
    '''
    @classmethod
    def setUpTestData(cls):
        '''
        Save a movie entry before running the tests to delete it 
        inside the tests using API requests
        '''
        cls.movie_id = create_test_movie()

    def test_delete_movie_valid_id(self):
        '''
        Test delete a movie information for the ID specified as URL param
        and return deleted data as JSON
        '''
        client = APIClient()
        url = f'/api/movies/{self.movie_id}'
        response = client.delete(url)

        self.assertEqual(len(Movie.objects.all()), 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data['id'], self.movie_id)
        self.assertEqual(response.data['name'], 'test_movie')
        self.assertEqual(response.data['desc'], 'tests movie desc')
        self.assertEqual(response.data['dor'], '1231-03-01')

    def test_delete_movie_with_invalid_id(self):
        '''
        Test 404 raised when trying to delete movie with invalid ID
        '''
        client = APIClient()
        url = f'/api/movies/invalid_request_id'
        response = client.put(url)

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Movie ID not found', status_code=404)