from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from games.models import Game, Review, Genre
from games.serializers import GameModelSerializer, ReviewSerializer, GenreSerializer


@api_view(['GET', 'POST'])
def game_list_create_api(request):
    """GET: Lista gier z optymalizacją ORM. POST: Tworzenie nowej gry."""
    if request.method == 'GET':
        games = Game.objects.select_related('genre').prefetch_related('platforms', 'reviews', 'reviews__author').all()

        genre_id = request.query_params.get('genre')
        if genre_id:
            games = games.filter(genre_id=genre_id)

        serializer = GameModelSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = GameModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def game_detail_api(request, pk):
    """CRUD dla pojedynczej gry z optymalizacją ORM."""
    queryset = Game.objects.select_related('genre').prefetch_related('platforms', 'reviews', 'reviews__author')
    game = get_object_or_404(queryset, pk=pk)

    if request.method == 'GET':
        serializer = GameModelSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = GameModelSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = GameModelSerializer(game, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_create_api(request):
    """GET: Lista recenzji. POST: Tworzenie nowej recenzji."""
    if request.method == 'GET':
        reviews = Review.objects.select_related('game', 'author').all()

        game_id = request.query_params.get('game')
        if game_id:
            reviews = reviews.filter(game_id=game_id)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def review_detail_api(request, pk):
    """CRUD dla pojedynczej recenzji."""
    queryset = Review.objects.select_related('game', 'author')
    review = get_object_or_404(queryset, pk=pk)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def genre_list_api(request):
    """Zwraca listę gatunków."""
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)