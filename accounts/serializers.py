from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CassUser


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=CassUser.objects.all(), message="사용 중인 아이디")
        ]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CassUser
        fields = ("username", "password", "password2", "name", "role")
        extra_kwarg = {"password": {"write_only": True}}

    def validate(self, info):
        if info["password"] != info.pop("password2"):
            raise serializers.ValidationError({"password2": "비밀번호 불일치"})
        return info

    def create(self, info):
        user = CassUser(username=info["username"], name=info["name"], role=info["role"])
        user.set_password(info["password"])
        user.save()
        return user
