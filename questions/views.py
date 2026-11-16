from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta

# Create your views here.

def paginate(objects_list, request, per_page=10):
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
    data["page_obj"] = paginate(get_questions(), request, 2)
    return render(request, "questions/index.html", data)

def hot_view(request):
    data = get_data(is_authentificated=False)
    data["page_obj"] = paginate(get_questions(), request, 2)
    return render(request, "questions/hot.html", data)

def tag_view(request, tag_name):
    data = get_data(is_authentificated=False)
    data["tag"] = tag_name
    data["page_obj"] = paginate(get_questions(), request, 2)
    return render(request, "questions/tag.html", data)

def question_view(request, question_id):
    data = get_data(is_authentificated=True)
    data["question"] = get_question(question_id)
    data["page_obj"] = paginate(get_answers(), request, 2)
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

def get_answers():
    return [
        {
            "id": 1,
            "author_name": "Uncle Sam",
            "author_avatar_url": "core/img/avatar.png",
            "text": "Для небольших проектов достаточно разбить код на папки components, pages, hooks и utils. Для крупных приложений удобно использовать feature-based структуру: каждая фича — отдельная папка со своими компонентами, хуками, стилями и тестами. Это упрощает навигацию и масштабирование.",
            "rating": 12,
            "user_vote": 1,
            "is_correct": True,
            "created_at": datetime.now() - timedelta(minutes=5),
        },
        {
            "id": 2,
            "author_name": "Darth Vader",
            "author_avatar_url": "core/img/avatar.png",
            "text": "Я бы посоветовал начать с официальной документации Create React App — там есть базовые рекомендации. А вообще структура сильно зависит от команды: главное, чтобы все придерживались одних договорённостей.",
            "rating": 0,
            "user_vote": 0,
            "is_correct": False,
            "created_at": datetime.now() - timedelta(minutes=30),
        },
        {
            "id": 3,
            "author_name": "Count Dooku",
            "author_avatar_url": "core/img/avatar.png",
            "text": "Посмотрите в сторону Next.js — там структура папок уже задана фреймворком (app/ или pages/), это сильно экономит время на соглашениях в команде.",
            "rating": -2,
            "user_vote": -1,
            "is_correct": False,
            "created_at": datetime.now() - timedelta(hours=1),
        },
    ]

def get_questions():
    return [
        {
            "id": 1,
            "title": "Как правильно организовать структуру проекта на React?",
            "text": "Только начал изучать React и не могу понять, как лучше разбить проект на компоненты и папки. Поделитесь опытом, как это делаете вы.",
            "author_avatar_url": "core/img/avatar.png",
            "tags": ["react", "frontend", "javascript"],
            "rating": 12,
            "user_vote": 0,
            "answers_count": 5,
            "created_at": datetime.now() - timedelta(hours=3),
        },
        {
            "id": 2,
            "title": "Как передавать данные между компонентами в React?",
            "text": "Не разберусь, когда использовать props, а когда контекст или сторонние стейт-менеджеры. Как выбрать подход?",
            "author_avatar_url": "core/img/avatar.png",
            "tags": ["react", "frontend"],
            "rating": 6,
            "user_vote": 1,
            "answers_count": 4,
            "created_at": datetime.now() - timedelta(hours=5),
        },
        {
            "id": 3,
            "title": "React useEffect вызывается бесконечно — как исправить?",
            "text": "В useEffect делаю setState, и компонент уходит в бесконечный цикл рендеров. В чём причина и как правильно?",
            "author_avatar_url": "core/img/avatar.png",
            "tags": ["react", "javascript"],
            "rating": 8,
            "user_vote": -1,
            "answers_count": 3,
            "created_at": datetime.now() - timedelta(hours=25),
        },
    ]

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