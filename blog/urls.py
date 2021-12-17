from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:q>/', views.GameSearch.as_view()),
    path('update_game/<int:pk>/', views.GameUpdate.as_view()),
    path('create_game/', views.GameCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.GameDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('', views.GameList.as_view()),
]
