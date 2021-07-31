from movies.models import Movie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .serializers import MovieSerializer


@api_view(['GET', 'POST'])
def create_movie(request):
    '''
    Add a new movie to the database from the JSON POST request
    '''
    try:
        if request.method == 'GET':
            Movie.objects.all().values()
            paginator = PageNumberPagination()
            paginator.page_size = 20
            movie_objects = Movie.objects.all()
            result_page = paginator.paginate_queryset(movie_objects, request)
            serializer = MovieSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
            
        if request.method == 'POST':
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

@api_view(['PUT'])
def movie_details(request, format=None, *args, **kwargs):
    movie_id = kwargs['id']
    try:
        movie_instance = Movie.objects.get(pk=movie_id)
    except Exception as e:
        raise NotFound(str('Movie ID not found'), code=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            unsafe_request = request.data
            unsafe_request.update({'id': kwargs['id']})
            serializer = MovieSerializer(data=unsafe_request)
            if serializer.is_valid(raise_exception=True):
                updated_movie = serializer.update(movie_instance, serializer.validated_data)
                response_dict = {
                    'id': updated_movie.id.hex,
                }
                response_dict.update(serializer.data)
                return Response(response_dict, status=status.HTTP_200_OK)
                
        except ValueError or TypeError as e:
            raise APIException(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
