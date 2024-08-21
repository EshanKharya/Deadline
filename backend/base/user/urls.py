from django.urls import path
from .views import LogoutView, RegisterView, ProfileView

urlpatterns = [
    path('logout/', LogoutView),
    path('register/', RegisterView),
    path('profile/', ProfileView.as_view()), 
]
