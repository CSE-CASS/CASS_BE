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
        success_flag = 0

        if serializer.is_valid():
            self.perform_create(serializer)
            user = self.perform_create(serializer)

            role = request.data.get("role")
            if role == "teacher":
                Teacher.objects.create(user=user)
            elif role == "teacher":
                Student.objects.create(user=user)
            success_flag = 1

            data = serializer.data
            data["success"] = success_flag

            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(
            {"success": success_flag, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


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

        return Response({"success": 1, "token": token.key, "username": user.username})
