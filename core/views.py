from django.shortcuts import render

# Create your views here.

def login_view(request):
    data = get_data()
    data["error"] = "Вы ввели неправильный логин или пароль"
    return render(request, "core/login.html", data)

def signup_view(request):
    data = get_data()
    data["errors"] = {
        "login": ["Некорректный логин"],
        "username": ["Некорректное имя пользователя"],
        "email": ["Некорректная почта"],
        "password": ["Пароли не совпадают"]
    }
    return render(request, "core/signup.html", data)

def profile_view(request):
    data = get_data(is_authentificated=True)
    data["errors"] = {
        "login": ["Некорректный логин"],
        "username": ["Некорректное имя пользователя"],
        "email": ["Некорректная почта"],
        "password": ["Пароли не совпадают"]
    }
    data["profile"] = {
        "login": "red_guy11",
        "username": "Red Guy",
        "email": "red@guy.com",
        "avatar_url": "avatar.png"
    }
    return render(request, "core/profile.html", data)

# Заглушки

def get_data(is_authentificated = False):
    data = {
        "popular_tags": get_tags(),
        "top_users": get_top_users()
    }
    if is_authentificated:
        data["user"] = {
            "is_authenticated": True,
            "username": "Red Guy",
            "avatar_url": "avatar.png"
        }
    else:
        data["user"] = {
            "is_authenticated": False
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
        "Tyler Durden"
    ]