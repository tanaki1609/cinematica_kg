from rest_framework import serializers
from .models import Film, Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        exclude = 'birthday'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    genres = serializers.SerializerMethodField()  # get_genres(film)

    class Meta:
        model = Film
        fields = 'id title release_year rating director genres reviews'.split()
        depth = 1

    def get_genres(self, film):
        return film.genre_names()
