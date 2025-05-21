from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer
from .models import Teacher, Student


class SignupAPIView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": 0, "errors": serializer.errors}, status=400)

        user = serializer.save()

        role = serializer.validated_data["role"]
        if role == "teacher":
            Teacher.objects.create(user=user)
        elif role == "student":
            Student.objects.create(user=user)

        data = serializer.data
        data["success"] = 1
        return Response(data, status=201)


class SigninAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid(raise_exception=False):
            return Response(
                {"success": 0, "message": "비밀번호 불일치"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "success": 1,
                "token": token.key,
                "username": user.username,
                "role": user.role,
            }
        )
