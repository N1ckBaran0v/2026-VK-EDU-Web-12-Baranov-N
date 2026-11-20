from django.contrib import admin
from django.db.models import Count

from .models import *

# Register your models here.

# ---------- Тег ----------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "questions_count")
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_questions_count=Count("question"))

    @admin.display(description="Вопросов", ordering="_questions_count")
    def questions_count(self, obj):
        return obj._questions_count


# ---------- Inline ответов в вопросе ----------
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ("content", "is_correct", "profile", "created_at")
    readonly_fields = ("created_at",)
    raw_id_fields = ("profile",)
    autocomplete_fields = ("profile",)
    show_change_link = True


# ---------- Вопрос ----------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "title", "profile", "created_at",
        "tags_list", "answers_count",
    )
    search_fields = ("title", "description", "tags__name", "profile__name")
    list_filter = ("created_at", "tags", "profile")
    list_select_related = ("profile",)
    raw_id_fields = ("profile",)
    autocomplete_fields = ("profile", "tags")
    filter_horizontal = ("tags",)   # удобный выбор M2M
    inlines = (AnswerInline,)
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("profile").prefetch_related("tags").annotate(
            _answers_count=Count("answer", distinct=True)
        )

    @admin.display(description="Теги")
    def tags_list(self, obj):
        # prefetch_related("tags") — без N+1
        return ", ".join(t.name for t in obj.tags.all()) or "—"

    @admin.display(description="Ответов", ordering="_answers_count")
    def answers_count(self, obj):
        return obj._answers_count


# ---------- Ответ ----------
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "id", "short_content", "question", "profile",
        "is_correct", "created_at",
    )
    search_fields = ("content", "question__title", "profile__name")
    list_filter = ("is_correct", "created_at")
    list_select_related = ("question", "profile")
    raw_id_fields = ("question", "profile")
    autocomplete_fields = ("question", "profile")
    date_hierarchy = "created_at"

    @admin.display(description="Текст ответа")
    def short_content(self, obj):
        return obj.content[:60] + ("…" if len(obj.content) > 60 else "")


# ---------- Лайк на вопрос ----------
@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "profile", "value", "value_label")
    search_fields = ("question__title", "profile__name")
    list_filter = ("value",)
    list_select_related = ("question", "profile")
    raw_id_fields = ("question", "profile")
    autocomplete_fields = ("question", "profile")

    @admin.display(description="Тип")
    def value_label(self, obj):
        return "Лайк" if obj.value == 1 else "Дизлайк"


# ---------- Лайк на ответ ----------
@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "answer", "profile", "value", "value_label")
    search_fields = ("answer__content", "profile__name")
    list_filter = ("value",)
    list_select_related = ("answer", "profile")
    raw_id_fields = ("answer", "profile")
    autocomplete_fields = ("answer", "profile")

    @admin.display(description="Тип")
    def value_label(self, obj):
        return "Лайк" if obj.value == 1 else "Дизлайк"