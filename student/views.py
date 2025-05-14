from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.models import Student
from teacher.models import Problem, Matching
from django.shortcuts import get_object_or_404


class StudentInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        student = get_object_or_404(Student, user=request.user)

        if student.matched:
            isMatched = 1

            match = Matching.objects.filter(student=student, status="matching").first()
            if match:
                teacher = match.teacher

                problems = list(
                    Problem.objects.filter(teacher=teacher).values_list(
                        "url", flat=True
                    )
                )
            else:
                problems = []
        else:
            isMatched = 0
            problems = []

        return Response({"isMatched": isMatched, "problems": problems})
