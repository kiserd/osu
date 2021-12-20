from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('puzzle/', views.puzzle),
    path('check/', views.check),
    path('puzzle_solved/', views.puzzle_solved)
]