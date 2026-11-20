from django.db import models

from django.conf import settings

# Create your models here.

class Tag(models.Model):
    name = models.TextField(verbose_name="Название тега", max_length=20)

class DefaultModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Автор", null=True)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        abstract = True

class Question(DefaultModel):
    title = models.TextField(verbose_name="Заголовок вопроса", max_length=50)
    description = models.TextField(verbose_name="Описание вопроса", max_length=1000)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)

class Answer(DefaultModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    content = models.TextField(verbose_name="Текст ответа", max_length=1000)
    is_correct = models.BooleanField(verbose_name="Ответ правильный")

class LikeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="Автор", null=True)
    value = models.IntegerField(verbose_name="Значение", choices=[(1, "Лайк"), (-1, "Дизлайк")], default = 1)
    
    class Meta:
        abstract = True

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")

    class Meta:
        constraints = [models.UniqueConstraint(name="user_question_like", fields=["user", "question"])]

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Вопрос")

    class Meta:
        constraints = [models.UniqueConstraint(name="user_answer_like", fields=["user", "answer"])]