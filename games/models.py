from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nazwa gatunku")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Slug (URL)")
    description = models.TextField(blank=True, verbose_name="Opis gatunku")

    class Meta:
        verbose_name = "Gatunek"
        verbose_name_plural = "Gatunki"
        ordering = ['name']

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nazwa platformy")
    slug = models.SlugField(max_length=60, unique=True, verbose_name="Slug platformy")
    manufacturer = models.CharField(max_length=100, verbose_name="Producent", blank=True)

    class Meta:
        verbose_name = "Platforma"
        verbose_name_plural = "Platformy"
        ordering = ['name']

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł gry")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Slug (URL)")
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="games",
        verbose_name="Gatunek"
    )
    platforms = models.ManyToManyField(
        Platform,
        related_name="games",
        blank=True,
        verbose_name="Platformy"
    )
    developer = models.CharField(max_length=150, verbose_name="Producent / Studio")
    release_date = models.DateField(verbose_name="Data wydania")
    description = models.TextField(verbose_name="Opis gry")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ostatnia aktualizacja")

    class Meta:
        verbose_name = "Gra"
        verbose_name_plural = "Gry"
        ordering = ['-release_date']

    def __str__(self):
        return f"{self.title} ({self.release_date.year})"


class Review(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Gra"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Autor recenzji"
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Ocena (1-10)"
    )
    title = models.CharField(max_length=200, verbose_name="Tytuł recenzji")
    content = models.TextField(verbose_name="Treść recenzji")
    is_approved = models.BooleanField(default=True, verbose_name="Zatwierdzona")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    class Meta:
        verbose_name = "Recenzja"
        verbose_name_plural = "Recenzje"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.rating}/10) – {self.game.title}"