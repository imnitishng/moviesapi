from django.db.models import fields
from .models import Movie
from rest_framework import serializers


class MovieResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        return {
            "id": instance.id.hex,
            "name": instance.name,
            "desc": instance.desc,
            "dor": instance.dor.strftime("%Y-%m-%d"),
        }


class MovieRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['name', 'desc', 'dor']    
