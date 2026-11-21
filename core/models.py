from django.db import models

from django.conf import settings

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь")
    name = models.TextField(verbose_name="отображаемое имя пользователя", max_length=150)
    avatar_url = models.ImageField(verbose_name="ссылка на аватар", upload_to="media/avatars", blank=True)

    class Meta:
        verbose_name="Профиль"
        verbose_name_plural="Профили"

    def __str__(self):
        return f"{self.name}"
