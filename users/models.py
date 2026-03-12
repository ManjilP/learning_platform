from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # AbstractUser gives us username, email, password out of the box
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)
