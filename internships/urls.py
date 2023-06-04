from django.urls import path
from .views import (
    LoginView,
    logout_view,
    user_interest,
    IndexView,
    SignUpView,
    GetInternshipsView,
)

urlpatterns = [
    path("signin/", LoginView.as_view(), name="signin"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", logout_view, name="logout"),
    path("", IndexView.as_view(), name="index"),
    path("internships/", GetInternshipsView.as_view(), name="internships"),
    path("user-interest/", user_interest, name="user-interest"),
]
