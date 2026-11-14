from rest_framework import serializers
from django.utils import timezone
from .models import Genre, Platform, Game, Review


class GenreSerializer(serializers.ModelSerializer):
    games_count = serializers.IntegerField(source='games.count', read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug', 'description', 'games_count']
        read_only_fields = ['id', 'games_count']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'slug', 'manufacturer']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    game_title = serializers.ReadOnlyField(source='game.title')

    class Meta:
        model = Review
        fields = ['id', 'game', 'game_title', 'author', 'author_username', 'rating', 'title', 'content', 'is_approved', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Ocena musi mieścić się w przedziale od 1 do 10.")
        return value


class GameModelSerializer(serializers.ModelSerializer):
    genre_name = serializers.ReadOnlyField(source='genre.name')
    platforms_details = PlatformSerializer(source='platforms', many=True, read_only=True)
    reviews_details = ReviewSerializer(source='reviews', many=True, read_only=True)
    platform_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Platform.objects.all(),
        source='platforms',
        write_only=True,
        required=False
    )
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id', 'title', 'slug', 'genre', 'genre_name',
            'platforms_details', 'platform_ids', 'developer',
            'release_date', 'description', 'average_rating',
            'reviews_count', 'reviews_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_average_rating(self, obj) -> float:
        """Oblicza średnią ocenę zatwierdzonych recenzji gry."""
        reviews = obj.reviews.filter(is_approved=True)
        if not reviews.exists():
            return 0.0
        total = sum(r.rating for r in reviews)
        return round(total / reviews.count(), 2)

    def get_reviews_count(self, obj) -> int:
        """Zwraca liczbę zatwierdzonych recenzji."""
        return obj.reviews.filter(is_approved=True).count()

    def validate_release_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Data wydania gry nie może być w przyszłości!")
        return value

    def validate_developer(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Nazwa studia produkcyjnego musi zawierać co najmniej 2 znaki.")
        return value.strip()
    def validate(self, attrs):
        title = attrs.get('title', getattr(self.instance, 'title', ''))
        description = attrs.get('description', getattr(self.instance, 'description', ''))
        release_date = attrs.get('release_date', getattr(self.instance, 'release_date', None))
        if release_date and release_date.year < 2000:
            if not any(keyword in description.lower() for keyword in ['klasyk', 'retro', 'pioniersk', 'nostalgi']):
                raise serializers.ValidationError({
                    "description": "Gry wydane przed 2000 rokiem muszą zawierać w opisie informację o swoim klasycznym/retro charakterze."
                })
        if any(w in title.lower() for w in ['remaster', 'remake']):
            if release_date and release_date.year < 2010:
                raise serializers.ValidationError({
                    "release_date": "Gry typu Remaster/Remake nie mogły zostać wydane przed 2010 rokiem."
                })

        return attrs