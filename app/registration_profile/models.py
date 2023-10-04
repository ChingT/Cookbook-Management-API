import random
import string

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


def code_generator(length=5, characters=string.digits):
    return "".join(random.choices(characters, k=length))


class RegistrationProfile(models.Model):
    code = models.CharField(max_length=5, default=code_generator)
    used = models.BooleanField(default=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"


@receiver(post_save, sender=User)
def create_registration_profile(sender, instance, **kwargs):
    profile, created = RegistrationProfile.objects.get_or_create(user=instance)
    if created:
        profile.save()
        print(f"RegistrationProfile created {profile}")
