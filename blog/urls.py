from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.GameDetail.as_view()),
    path('', views.GameList.as_view()),
]
