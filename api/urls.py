# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ask-question/', views.ask_question_api, name='ask_question_api'),
]