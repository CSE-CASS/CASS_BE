from django.db import models
from accounts.models import Teacher, Student


class Problem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    url = models.URLField()

    submits = models.TextField(null=True)

    def __str__(self):
        return f"문제: {self.url} - {self.teacher.user.name}"


class Matching(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "대기중"),
            ("matching", "매칭됨"),
        ],
        default="pending",
    )
