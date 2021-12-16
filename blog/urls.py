from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.GameDetail.as_view()),
    path('', views.GameList.as_view()),
]
