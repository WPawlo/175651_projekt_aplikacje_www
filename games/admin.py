from django.contrib import admin
from .models import Genre, Platform, Game, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'games_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description="Liczba gier")
    def games_count(self, obj):
        return obj.games.count()


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'manufacturer')
    search_fields = ('name', 'manufacturer')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'developer', 'release_date')
    list_filter = ('genre', 'platforms', 'release_date')
    search_fields = ('title', 'developer', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('platforms',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'author', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'game__title')
    list_editable = ('is_approved',)