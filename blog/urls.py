from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:q>/', views.GameSearch.as_view()),     # 검색페이지
    path('update_game/<int:pk>/', views.GameUpdate.as_view()),  # 수정페이지
    path('create_game/', views.GameCreate.as_view()),   # 등록 페이지
    path('category/<str:slug>/', views.category_page),   # 카테고리 페이지
    path('<int:pk>/', views.GameDetail.as_view()),  # 상세 페이지
    path('<int:pk>/new_comment/', views.new_comment),    # 댓글
    path('', views.GameList.as_view()),  # 목록 페이지
]
