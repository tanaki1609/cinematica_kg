from rest_framework import serializers
from .models import Film


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        # fields = ['id', 'title', 'rating', 'created']
        fields = 'id title release_year rating'.split()
        # fields = '__all__'
        # exclude = 'id rating'.split()
