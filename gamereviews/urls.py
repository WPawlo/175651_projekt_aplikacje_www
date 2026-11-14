"""
URL configuration for gamereviews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import api_views
from django.contrib import admin

app_name = 'games'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/games/', api_views.game_list_create_api, name='api-game-list-create'),
    path('api/games/<int:pk>/', api_views.game_detail_api, name='api-game-detail'),
    path('api/reviews/', api_views.review_list_create_api, name='api-review-list-create'),
    path('api/reviews/<int:pk>/', api_views.review_detail_api, name='api-review-detail'),
    path('api/genres/', api_views.genre_list_api, name='api-genre-list'),
]