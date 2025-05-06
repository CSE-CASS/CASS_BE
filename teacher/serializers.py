from rest_framework import serializers
from accounts.models import Teacher, Student
from .models import Problem, Matching


class ProblemSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()

    students = serializers.SlugRelatedField(
        queryset=Student.objects.all(), slug_field="user__username", many=True
    )

    class Meta:
        model = Problem
        fields = ["url"]


class MatchingSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    student = serializers.SlugRelatedField(
        queryset=Student.objects.all(), slug_field="user__username"
    )

    class Meta:
        model = Matching
        fields = ["teacher", "student", "status"]
