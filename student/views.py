from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.models import Student, Teacher, CassUser
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


class MatchingRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        teacher_id = request.data.get("teacher_id")

        try:
            teacher = Teacher.objects.get(user__username=teacher_id)
        except Teacher.DoesNotExist:
            return Response(
                {
                    "success": 0,
                    "msg": "요청실패 - 존재하지않는 선생",
                },
                status=400,
            )

        if Matching.objects.filter(
            teacher=teacher, student=student, status="pending"
        ).exists():
            return Response(
                {
                    "success": 0,
                    "msg": "요청실패 - 수락 대기중",
                },
                status=400,
            )

        Matching.objects.create(teacher=teacher, student=student)
        return Response(
            {
                "success": 1,
                "msg": "요청성공",
            },
            status=201,
        )
