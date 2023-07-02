from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

def home(request: WSGIRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in.")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

# If you need separate login page so you need this function
# def login_user(request):
#     pass
def logout_user(request: WSGIRequest):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request: WSGIRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Auth and login
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            messages.success(request, "You have Successfully registered.")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})
