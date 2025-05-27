from django.urls import path
from .views import GenerateSummaryView, GenerateBulletPointsView, RegisterUserView, GenerateQuizView
from .views import LogoutUserView, summary_ui_view, bullet_ui_view

urlpatterns = [
    path('generate-summary/', GenerateSummaryView.as_view()),
    path('generate-bullet-points/', GenerateBulletPointsView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('quiz/', GenerateQuizView.as_view(), name='generate-quiz'),
    path("logout/", LogoutUserView.as_view(), name="api-logout"),
    path("ui/summary/", summary_ui_view, name="summary-ui"),
    path("ui/bullets/", bullet_ui_view, name="bullets-ui"),
]
# This file defines the URL patterns for the summarizer app.