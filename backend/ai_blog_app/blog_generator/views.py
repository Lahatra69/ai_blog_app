from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data["link"]
            return JsonResponse({"content": yt_link})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data sent."}, status=400)

        # get yt title

        # get transcript

        # use openai to generate blog content

        # save article to db

        # return blog article as response
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(
                request, "login.html", {"error_mesage": "Invalid username or password"}
            )
    return render(request, "login.html")


def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeatPassword = request.POST.get("repeatPassword")

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect("/")
            except:
                return render(
                    request, "signup.html", {"error_mesage": "Error creating user"}
                )
        else:
            return render(
                request, "signup.html", {"error_mesage": "Password doesn't match"}
            )

    return render(request, "signup.html")


def user_logout(request):
    logout(request)
    return redirect("/")
