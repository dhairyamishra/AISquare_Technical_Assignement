from django.urls import path
from .views import GenerateSummaryView, GenerateBulletPointsView, RegisterUserView, GenerateQuizView
from .views import LogoutUserView

urlpatterns = [
    path('generate-summary/', GenerateSummaryView.as_view()),
    path('generate-bullet-points/', GenerateBulletPointsView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('quiz/', GenerateQuizView.as_view(), name='generate-quiz'),
    path("logout/", LogoutUserView.as_view(), name="api-logout"),
]
# This file defines the URL patterns for the summarizer app.