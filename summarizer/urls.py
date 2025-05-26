from django.urls import path
from .views import GenerateSummaryView, GenerateBulletPointsView

urlpatterns = [
    path('generate-summary/', GenerateSummaryView.as_view()),
    path('generate-bullet-points/', GenerateBulletPointsView.as_view()),
]
# This file defines the URL patterns for the summarizer app.