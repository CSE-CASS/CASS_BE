from django.urls import path
from . import views
from .views import gpt_request

urlpatterns = [
    path('chat/', gpt_request, name='gpt_request'),
]