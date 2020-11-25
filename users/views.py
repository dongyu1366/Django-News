from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import UserForm


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            form = UserForm()
            messages.warning(request, f'Incorrect username or password')
            return render(request, "users/signin.html", {"form": form})
    else:
        form = UserForm()
        return render(request, "users/signin.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("index")


def user_register(request):
    if request.method == "POST":
        form = UserForm(data=request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("index")
        else:
            print(form.errors)
    else:
        form = UserForm()

    return render(request, "users/signup.html", {"form": form})
