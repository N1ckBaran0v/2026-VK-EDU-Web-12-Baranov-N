from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from .models import *

# Create your views here.

def paginate(objects_list, request, per_page=20):
    page_num = request.GET.get("page", 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages if int(page_num) > paginator.num_pages else 1)
    return page

def index_view(request):
    data = get_data(is_authentificated=False)
    data["page_obj"] = paginate(Question.objects.get_new(), request)
    return render(request, "questions/index.html", data)

def hot_view(request):
    data = get_data(is_authentificated=False)
    data["page_obj"] = paginate(Question.objects.get_hot(), request)
    return render(request, "questions/hot.html", data)

def tag_view(request, tag_slug):
    data = get_data(is_authentificated=False)
    data["tag"] = get_object_or_404(Tag, slug=tag_slug)
    data["page_obj"] = paginate(Question.objects.get_by_tag(tag_slug), request)
    return render(request, "questions/tag.html", data)

def question_view(request, question_id):
    data = get_data(is_authentificated=True)
    data["question"] = get_object_or_404(Question, pk=question_id)
    data["page_obj"] = paginate(Answer.objects.get_queryset(), request)
    data["can_mark_correct"] = True
    data["errors"] = {}
    return render(request, "questions/question.html", data)

def ask_view(request):
    data = get_data(is_authentificated=True)
    data["errors"] = {}
    return render(request, "questions/ask.html", data)

# Заглушки

def get_question(question_id):
    return {
        "id": question_id,
        "title": "Как правильно организовать структуру проекта на React?",
        "text": "Только начал изучать React и не могу понять, как лучше разбить проект на компоненты и папки. Поделитесь опытом, как это делаете вы. Интересует и структура для небольших проектов, и для крупных приложений с множеством модулей.",
        "author_name": "Red Guy",
        "author_avatar_url": "core/img/avatar.png",
        "created_at": datetime.now() - timedelta(hours=3),
        "tags": ["react", "frontend", "javascript"],
        "rating": 6,
        "user_vote": 0,
        "answers_count": 5,
    }

def get_data(is_authentificated=False):
    data = {
        "popular_tags": get_tags(),
        "top_users": get_top_users(),
    }
    if is_authentificated:
        data["user"] = {
            "is_authenticated": True,
            "username": "Red Guy",
            "avatar_url": "core/img/avatar.png",
        }
    else:
        data["user"] = {
            "is_authenticated": False,
        }
    return data

def get_tags():
    return [
        "frontend",
        "backend",
        "devops",
        "security",
        "testing",
        "docker",
        "kubernetes",
        "postgresql",
        "mongodb",
        "redis",
        "graphql",
        "rest-api",
        "microservices",
        "machine-learning",
        "algorithms",
        "git",
        "linux",
        "nginx",
        "ci-cd",
        "cloud",
    ]


def get_top_users():
    return [
        "Uncle Sam",
        "Red Guy",
        "Count Dooku",
        "S. Holmes",
        "Darth Vader",
        "Lara Croft",
        "Gordon Freeman",
        "Princess Leia",
        "W. White",
        "Tyler Durden",
    ]