from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('ch1', views.ch1, name="ch1"),
    path('ch2', views.ch2, name="ch2"),
    path('devInfo', views.devInfo, name="devInfo"),
    path('chatanswer', views.chatanswer, name="chatanswer"),
]