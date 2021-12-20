from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), # 홈페이지
    path('about_me/', views.about_me), # 마이페이지
    path('amuse/', views.amuse) # 회사소개 페이지
]