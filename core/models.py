import os
import uuid

from django.db import models

from django.conf import settings

# Create your models here.

def avatar_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"avatars/{uuid.uuid4().hex}{ext}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь")
    name = models.TextField(verbose_name="отображаемое имя пользователя", max_length=150)
    avatar_url = models.ImageField(verbose_name="ссылка на аватар", upload_to=avatar_upload_to, blank=True)

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"

    def __str__(self):
        return f"{self.name}"
