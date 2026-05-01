from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Film
from .serializers import FilmListSerializer, FilmDetailSerializer
from rest_framework import status


@api_view(['GET'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except:
        return Response(data={'message': 'film not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = FilmDetailSerializer(film, many=False).data
    return Response(data=data)


@api_view(['GET'])
def film_list_api_view(request):
    # step 1: collect films (QuerySet)
    films = (Film.objects.select_related('director')
             .prefetch_related('genres', 'reviews').all())

    # step 2: reformat films to list of dictionary
    data = FilmListSerializer(films, many=True).data

    # step 3: return response
    return Response(
        data=data,  # list, dict
    )
