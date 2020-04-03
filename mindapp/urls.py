from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('level',views.answer, name="situation"),
    path('leaderboard',views.leaderboard,name="leaderboard"),
    path('rules',views.rules,name="rules"),
    path('options',views.options,name="options"),
    path('subjective',views.subjective,name="subjective")
]