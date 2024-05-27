from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
import openai
import os
import assemblyai as aai


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


def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title


def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = "your-api"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    return transcriber.text


def generate_blog_from_transcription(transcription):
    openai.api_key = "your-api"

    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
    )

    generated_content = response.choices[0].text.strip()

    return generated_content


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
