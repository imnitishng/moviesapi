from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.decorators import api_view

from .serializers import MovieSerializer


@api_view(['POST'])
def create_movie(request):
    '''
    Add a new movie to the database from the JSON POST request
    '''
    try:
        unsafe_request = request.data
        serializer = MovieSerializer(data=unsafe_request)
        if serializer.is_valid(raise_exception=True):
            saved_movie = serializer.save()
            response_dict = {
                'id': saved_movie.id.hex,
            }
            response_dict.update(serializer.data)
            return Response(response_dict, status=status.HTTP_201_CREATED)

    except ValueError or TypeError as e:
        raise APIException(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
