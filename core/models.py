from django.db import models

from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.TextField(verbose_name="Имя пользователя", max_length=150)
    avatar_url = models.ImageField(verbose_name="Ссылка на аватар", upload_to="media/avatars", blank=True)

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"
