from django.shortcuts import render

# Create your views here.

def index_view(request):
    data = get_data(is_authentificated=False)
    data["page_obj"] = get_page_obj(get_questions)
    return render(request, "questions/index.html", data)

def hot_view(request):
    data = get_data(is_authentificated=False)
    data["page_obj"] = get_page_obj(get_questions)
    return render(request, "questions/hot.html", data)

def tag_view(request, tag):
    data = get_data(is_authentificated=False)
    data["tag"] = tag
    data["page_obj"] = get_page_obj(get_questions)
    return render(request, "questions/tag.html", data)

def question_view(request, pk):
    data = get_data(is_authentificated=True)
    data["question"] = get_question(pk)
    data["page_obj"] = get_page_obj(get_answers)
    data["can_mark_correct"] = True
    data["errors"] = {}
    return render(request, "questions/question.html", data)

def ask_view(request):
    data = get_data(is_authentificated=True)
    data["errors"] = {}
    return render(request, "questions/ask.html", data)

# Заглушки

def get_page_obj(func):
    return {
        "items": func(),
        "paginator": {
            "num_pages": 2,
            "page_range": [1, 2],
        },
        "number": 1,
        "has_previous": False,
        "previous_page_number": 1,
        "has_next": True,
        "next_page_number": 2,
    }

def get_question(pk):
    return {
        "id": pk,
        "title": "Как правильно организовать структуру проекта на React?",
        "text": "Только начал изучать React и не могу понять, как лучше разбить проект на компоненты и папки. Поделитесь опытом, как это делаете вы. Интересует и структура для небольших проектов, и для крупных приложений с множеством модулей.",
        "author_name": "Red Guy",
        "author_avatar_url": "avatar.png",
        "created_at_label": "5 минут назад",
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
            "author_avatar_url": "avatar.png",
            "text": "Для небольших проектов достаточно разбить код на папки components, pages, hooks и utils. Для крупных приложений удобно использовать feature-based структуру: каждая фича — отдельная папка со своими компонентами, хуками, стилями и тестами. Это упрощает навигацию и масштабирование.",
            "rating": 12,
            "user_vote": 1,
            "is_correct": True,
            "created_at_label": "3 минуты назад",
        },
        {
            "id": 2,
            "author_name": "Darth Vader",
            "author_avatar_url": "avatar.png",
            "text": "Я бы посоветовал начать с официальной документации Create React App — там есть базовые рекомендации. А вообще структура сильно зависит от команды: главное, чтобы все придерживались одних договорённостей.",
            "rating": 0,
            "user_vote": 0,
            "is_correct": False,
            "created_at_label": "4 минуты назад",
        },
        {
            "id": 3,
            "author_name": "Count Dooku",
            "author_avatar_url": "avatar.png",
            "text": "Посмотрите в сторону Next.js — там структура папок уже задана фреймворком (app/ или pages/), это сильно экономит время на соглашениях в команде.",
            "rating": -2,
            "user_vote": -1,
            "is_correct": False,
            "created_at_label": "4 минуты назад",
        },
    ]

def get_questions():
    return [
        {
            "id": 1,
            "title": "Как правильно организовать структуру проекта на React?",
            "text": "Только начал изучать React и не могу понять, как лучше разбить проект на компоненты и папки. Поделитесь опытом, как это делаете вы.",
            "author_avatar_url": "avatar.png",
            "tags": ["react", "frontend", "javascript"],
            "rating": 12,
            "user_vote": 0,
            "answers_count": 5,
            "created_at_label": "5 минут назад",
        },
        {
            "id": 2,
            "title": "Как передавать данные между компонентами в React?",
            "text": "Не разберусь, когда использовать props, а когда контекст или сторонние стейт-менеджеры. Как выбрать подход?",
            "author_avatar_url": "avatar.png",
            "tags": ["react", "frontend"],
            "rating": 6,
            "user_vote": 1,
            "answers_count": 4,
            "created_at_label": "1 час назад",
        },
        {
            "id": 3,
            "title": "React useEffect вызывается бесконечно — как исправить?",
            "text": "В useEffect делаю setState, и компонент уходит в бесконечный цикл рендеров. В чём причина и как правильно?",
            "author_avatar_url": "avatar.png",
            "tags": ["react", "javascript"],
            "rating": 8,
            "user_vote": -1,
            "answers_count": 3,
            "created_at_label": "вчера",
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
            "avatar_url": "avatar.png",
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