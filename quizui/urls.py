from django.urls import path
from .views import play_quiz

urlpatterns = [
    path("play/", play_quiz, name="play-quiz")
]
