from django.db import models
from django.contrib.auth.models import AbstractUser


class CassUser(AbstractUser):
    ROLE_CHOICES = [
        ("teacher", "선생"),
        ("student", "학생"),
    ]
    name = models.CharField("이름", max_length=20)
    role = models.CharField("역할", max_length=10, choices=ROLE_CHOICES)


class Teacher(models.Model):
    user = models.ForeignKey(CassUser, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.ForeignKey(CassUser, on_delete=models.CASCADE)
    matched = models.BooleanField(default=False)
