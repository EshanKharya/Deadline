from django.urls import path
from .views import (
    ProjectView,
    ProjectDetail,
    ProjectContributorDetail,
    ProjectContributors,
)

urlpatterns = [
    path("", ProjectView.as_view()),
    path("<uuid:pid>/", ProjectDetail.as_view()),
    path("<uuid:pid>/contributors/", ProjectContributors.as_view()),
    path("<uuid:pid>/contributors/<uuid:cid>/", ProjectContributorDetail.as_view()),
]
