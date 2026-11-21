from django.db import models
from django.db.models.aggregates import Count, Sum

from core.models import Profile

# Create your models here.

class Tag(models.Model):
    name = models.TextField(verbose_name="название тега", max_length=20, unique=True)
    slug = models.TextField(verbose_name="ссылка на тег", max_length=20, unique=True)

    class Meta:
        verbose_name="Тег"
        verbose_name_plural="Теги"

    def __str__(self):
        return f"{self.name}"

class DefaultModel(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Автор", null=True)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)

    class Meta:
        abstract = True

class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            rating=Sum("questionlike__value", default=0), 
            answers_count=Count("answer", distinct=True)
        ).select_related("profile").prefetch_related("tags")

    def get_new(self):
        return self.get_queryset().order_by("-created_at")

    def get_hot(self):
        return self.get_queryset().order_by("-rating").order_by("-created_at")

    def get_by_tag(self, tag):
        return self.get_queryset().filter(tags__slug=tag).order_by("-created_at")

class Question(DefaultModel):
    title = models.TextField(verbose_name="Заголовок вопроса", max_length=50)
    description = models.TextField(verbose_name="Описание вопроса", max_length=1000)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)

    objects = QuestionManager()

    class Meta:
        verbose_name="Вопрос"
        verbose_name_plural="Вопросы"

    def __str__(self):
        return f"Вопрос {self.pk} \"{self.title}\""

class AnswerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            rating=Sum("answerlike__value", default=0)
        ).select_related("profile").order_by("-rating").order_by("-created_at");

class Answer(DefaultModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    content = models.TextField(verbose_name="Текст ответа", max_length=1000)
    is_correct = models.BooleanField(verbose_name="Ответ правильный")

    objects = AnswerManager()

    class Meta:
        verbose_name="Ответ"
        verbose_name_plural="Ответы"

    def __str__(self):
        return f"Ответ {self.pk} от {self.profile.name}"

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

    def __str__(self):
        return f"Реакция от {self.profile.name} на вопрос от {self.question.profile.name}"

class AnswerLike(LikeModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Вопрос")

    class Meta:
        constraints = [models.UniqueConstraint(name="user_answer_like", fields=["profile", "answer"])]
        verbose_name="Лайк на ответ"
        verbose_name_plural="Лайки на ответы"

    def __str__(self):
        return f"Реакция от {self.profile.name} на ответ от {self.answer.profile.name}"