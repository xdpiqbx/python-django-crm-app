from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

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
        records = Record.objects.all()
        return render(request, 'home.html', {'records': records})
        # return render(request, 'home.html', {})

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

def customer_record(request: WSGIRequest, pk: int):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': customer_record})
    else:
        messages.success(request, "You must been login to view this page")
        return redirect('home')

def delete_record(request: WSGIRequest, pk: int):
    if request.user.is_authenticated:
        del_record = Record.objects.get(id=pk)
        del_record.delete()
        messages.success(request, "Record deleted Successfully")
        return redirect('home')
    else:
        messages.success(request, "You must been login to to do that")
        return redirect('home')

def add_record(request: WSGIRequest):
    return render(request, 'add_record.html', {})
