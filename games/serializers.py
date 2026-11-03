from rest_framework import serializers
from .models import Game, Genre


class GameSerializer(serializers.Serializer):
    """
    Bazowy serializator dla modelu Game (zgodnie z wymogami Lab 4).
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=200)
    slug = serializers.SlugField(required=True, max_length=220)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        source='genre'
    )
    developer = serializers.CharField(max_length=150)
    release_date = serializers.DateField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.developer = validated_data.get('developer', instance.developer)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance