from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_game_page),
    path('', views.index)
]