from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('level',views.answer, name="situation"),
    path('leaderboard',views.leaderboard,name="leaderboard"),
    path('rules',views.rules,name="rules"),
    path('logout',views.logout_view,name="logout"),
    path('plswait',views.pls_wait,name="plswait")
]