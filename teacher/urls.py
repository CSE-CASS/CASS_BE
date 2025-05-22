from django.urls import path
from . import views

urlpatterns = [
    path("info", views.TeacherInfo.as_view()),
    path("m_accept/<str:student_id>", views.MatchingAccept.as_view()),
    path("m_reject/<str:student_id>", views.MatchingReject.as_view()),
    path("delete_student/<str:student_id>", views.DeleteStudent.as_view()),
    path("add_problem", views.AddProblem.as_view()),
    path("delete_problem/<int:problem_id>", views.DeleteProblem.as_view()),
    path("check/<int:problem_id>", views.SubmitCheck.as_view()),
]
