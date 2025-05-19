from django.urls import path
from . import views

urlpatterns = [
    path("info", views.TeacherInfo.as_view()),
    path("m_accept/<str:student_id>", views.MatchingAccept.as_view()),
    path("m_reject/<str:student_id>", views.MatchingReject.as_view()),
    path("add_problem", views.AddProblem.as_view()),
]
