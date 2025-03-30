from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from mainapp.utils import util

@api_view(['POST'])
def get_song(request):
    data = request.data
    song = data["song"]
    artist = data["artist"]
    a = util.testone(song, artist)
    return Response(a, status=status.HTTP_200_OK)
