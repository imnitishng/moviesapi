from django.test import TestCase
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
    @classmethod
    def setUpTestData(cls):
        '''
        Save a movie entry before running the tests to edit it 
        inside the tests using API requests
        '''
        create_bulk_test_movies()

