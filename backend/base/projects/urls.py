from django.urls import path
from .views import ProjectView, ProjectDetail

urlpatterns = [
    path("", ProjectView.as_view()),
    path("<uuid:pid>/", ProjectDetail.as_view())
]
