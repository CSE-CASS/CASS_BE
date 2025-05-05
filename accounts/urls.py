from django.urls import path
from .views import SignupAPIView, SigninAPIView

urlpatterns = [
    path("signup", SignupAPIView.as_view()),
    path("signin", SigninAPIView.as_view()),
]
