from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from accounts.models import Teacher, Student
from .models import Problem, Matching
from .serializers import ProblemSerializer, MatchingSerializer
from django.shortcuts import get_object_or_404


class TeacherInfo(APIView):
    authentication_classses = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user)

        pending = Matching.objects.filter(teacher=teacher, status="pending")
        pending_students = [matching.student for matching in pending]
        pending_students_data = [
            {"username": student.user.username, "name": student.user.name}
            for student in pending_students
        ]

        matched = Matching.objects.filter(teacher=teacher, status="matching")
        matched_students = [matching.student for matching in matched]
        matched_students_data = [
            {"username": student.user.username, "name": student.user.name}
            for student in matched_students
        ]

        problems = Problem.objects.filter(teacher=teacher)
        problem_urls = [{"url": problem.url} for problem in problems]

        return Response(
            {
                "pending_students": pending_students_data,
                "matching_students": matched_students_data,
                "problems": problem_urls,
            }
        )
