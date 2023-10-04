import random
import string

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def code_generator(length=5, characters=string.digits):
    return "".join(random.choices(characters, k=length))


class RegistrationProfile(models.Model):
    code = models.CharField(max_length=5, default=code_generator)
    used = models.BooleanField(default=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"
