from django.urls import path
from . import views

urlpatterns = [
    path('update_game/<int:pk>/', views.GameUpdate.as_view()),
    path('create_game/', views.GameCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.GameDetail.as_view()),
    path('', views.GameList.as_view()),
]
