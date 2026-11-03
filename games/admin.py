from django.contrib import admin
from .models import Genre, Game, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'games_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description="Liczba gier")
    def games_count(self, obj):
        return obj.games.count()


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'developer', 'release_date')
    list_filter = ('genre', 'release_date')
    search_fields = ('title', 'developer')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('title', 'content')