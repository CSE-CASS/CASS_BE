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

                qs = Problem.objects.filter(teacher=teacher).values("id", "name", "url")
                problems = list(qs)
            else:
                problems = []
        else:
            isMatched = 0
            problems = []

        return Response(
            {
                "student_id": student.user.username,
                "isMatched": isMatched,
                "problems": problems,
            }
        )


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


class Submit(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, problem_id, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        problem = get_object_or_404(Problem, id=problem_id)

        if not problem.students.filter(pk=student.pk).exists():
            return Response(
                {"success": 0, "msg": "권한이 없는 문제"},
                status=403,
            )

        code = request.data.get("code")
        if code is None:
            return Response(
                {"success": 0, "msg": "제출 실패 - 코드가 없습니다"},
                status=400,
            )

        raw = problem.submits or ""
        delimiter = "===\n"
        entries = [e for e in raw.split(delimiter) if e.strip()]
        entries = [e for e in entries if e.splitlines()[0] != student.user.username]

        # 5) 새 제출 항목 추가
        new_entry = f"{student.user.username}\n{code}\n"
        entries.append(new_entry)

        # 6) 다시 text 필드에 저장
        problem.submits = delimiter.join(entries)
        problem.save()

        # 7) 응답
        return Response(
            {"success": 1, "msg": "제출 완료"},
            status=200,
        )
