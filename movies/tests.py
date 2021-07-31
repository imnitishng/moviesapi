from re import M
from django.test import TestCase
from rest_framework.test import APIClient


class TestMoviesPOST(TestCase):
    '''
    Test POST operations for movies
    '''

    url = '/api/movies/add'

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

