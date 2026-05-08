from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


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


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=255)
    text = serializers.CharField(required=False)
    release_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField(default=False)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):  # [1,2,1,1,1,1]
        genres = list(set(genres))  # [1,2]
        genres_db = Genre.objects.filter(id__in=genres)  # [1,2]
        if len(genres_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres
