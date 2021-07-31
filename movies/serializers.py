from django.db.models import fields
from .models import Movie
from rest_framework import serializers


class MovieJSONSerializer(serializers.Serializer):
    name = serializers.CharField()
    desc = serializers.CharField()
    dor = serializers.DateField(format="%d-%m-%Y")
    

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['name', 'desc', 'dor']    
