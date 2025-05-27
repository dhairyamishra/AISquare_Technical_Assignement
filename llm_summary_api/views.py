from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request, "home.html")

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "registration/register.html", {"error": "Both fields are required."})
        if User.objects.filter(username=username).exists():
            return render(request, "registration/register.html", {"error": "Username already exists."})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")
    return render(request, "registration/register.html")