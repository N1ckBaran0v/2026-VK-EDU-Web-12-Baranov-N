from django.db import models

from core.models import Profile

# Create your models here.

class Tag(models.Model):
    name = models.TextField(verbose_name="Название тега", max_length=20, unique=True)

    class Meta:
        verbose_name="Тег"
        verbose_name_plural="Теги"

    def __str__(self):
        return f"Тег \"{self.name}\""

class DefaultModel(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Автор", null=True)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        abstract = True

class Question(DefaultModel):
    title = models.TextField(verbose_name="Заголовок вопроса", max_length=50)
    description = models.TextField(verbose_name="Описание вопроса", max_length=1000)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)

    class Meta:
        verbose_name="Вопрос"
        verbose_name_plural="Вопросы"

class Answer(DefaultModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    content = models.TextField(verbose_name="Текст ответа", max_length=1000)
    is_correct = models.BooleanField(verbose_name="Ответ правильный")

    class Meta:
        verbose_name="Ответ"
        verbose_name_plural="Ответы"

class LikeModel(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Автор", null=True)
    value = models.IntegerField(verbose_name="Значение", choices=[(1, "Лайк"), (-1, "Дизлайк")], default = 1)
    
    class Meta:
        abstract = True

class QuestionLike(LikeModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")

    class Meta:
        constraints = [models.UniqueConstraint(name="user_question_like", fields=["profile", "question"])]
        verbose_name="Лайк на вопрос"
        verbose_name_plural="Лайки на вопросы"

class AnswerLike(LikeModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Вопрос")

    class Meta:
        constraints = [models.UniqueConstraint(name="user_answer_like", fields=["profile", "answer"])]
        verbose_name="Лайк на ответ"
        verbose_name_plural="Лайки на ответы"