from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, "index.html")


def user_login(request):
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
    pass
