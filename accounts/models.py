from django.db import models
from django.contrib.auth.models import AbstractUser


class CassUser(AbstractUser):
    name = models.CharField("이름", max_length=20)
    role = models.BooleanField("역할", default=False)
