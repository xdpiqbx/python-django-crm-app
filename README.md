# python-django-crm-app

## Work with Env variables
1. `pip install django-environ`
2. create `.env` file in the same folder with `settings.py`
```
DB_ENGINE=django.db.backends.postgresql
DB_USER=john
DB_PASSWORD=john@#687
```
3. use vars from `.env`
```python
import environ
env = environ.Env()
environ.Env.read_env()
print(env.str('DB_ENGINE'))
print(env.str('DB_USER'))
print(env.str('DB_PASSWORD'))
```

## Set up `venv`
- cd -> `...go\001-python-django-crm-app`
- Create venv -> `python -m venv crm-venv`
- Activate venv (in nix systems) -> `source .\crm-venv\Scripts\activate`
- Activate venv (in win systems) -> `.\crm-venv\Scripts\activate`

## Install
- `pip install django`
- Clear work with PG -> `pip install postgres`
- [Standart!](https://pypi.org/project/psycopg2/) -> `pip install psycopg2`
- [`pip install django-environ`](https://django-environ.readthedocs.io/en/latest/install.html)

## Create project
- `django-admin startproject crm_app`
- `cd ./crm_app`
- `python manage.py startapp website`

## Settings.py
`->` `(....\001-python-django-crm-app\crm_app\crm_app\settings.py)`
```python
INSTALLED_APPS = [
    # .... 
    'django.contrib.staticfiles',
    'website' # <- Add website because of -> python manage.py startapp >>> website <<<
]
```
Configure databases
```python
# Default is
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
```python
# PostgreSQL

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'db_name',
        'USER': 'db_username',
        'PASSWORD': 'p@$$w0rD',
        'HOST': 'db ip address',
        'PORT': '658347'
    }
}
```

## Test your connection to postgres DB
Create some file (random name) like `db_connection.py`
```python
# Test your connection to postgres DB
import psycopg2
conn = psycopg2.connect(
    dbname="db_name",
    host="db ip address",
    port="658347",
    user="db_username",
    password="p@$$w0rD",
)
cur = conn.cursor()
print(cur)
cur.close()
conn.close()
```

## Create db structure for django app:
`cd ...hon/Django/001-python-django-crm-app/crm_app`
```code
python manage.py migrate
```
in console you will see...
```console
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
....
Applying sessions.0001_initial... OK
```

## Create superuser
`winpty python manage.py createsuperuser`

## First rum
`python manage.py runserver`

## Creation Web page
0. In App we already have `./crm_app/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls'))  # Add this line
]
```
1. Create URL `./website/urls.py`
```python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
]
```
2. Create View in `./website/views.py`
```python
from django.shortcuts import render
def home(request):
    return render(request, 'home.html', {})
```
3. Create Template `./website/templates/home.html`
```html
<h1>Hello from Home page</h1>
```

## About templates
1. create `base.html` it something like root or entry point
```html
  <body>
    {% include 'navbar.html' %}
    <div class="container">
      {% block content %}
      {% endblock %}
    </div>
  </body>
```
2. Navbar was included to `base.html` and this how to add link `href="{% url 'home' %}`
```html
<a class="navbar-brand" href="{% url 'home' %}">Django CRM</a>
```
3. Create `home.html`
```html
{% extends 'base.html' %}
{% block content %}
<h1>Hello from Home page</h1>
{% endblock %}
```

## `Login` & `Logout`
- URLs
```python
urlpatterns = [
    path('', views.home, name="home"),
    # path('login/', views.login_user, name="login"), # I will use Home page for login
    path('logout/', views.logout_user, name="logout"),
]
```
- View.s Add to site `views.py`
```python
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')
```
- Template `home.html`
```html
{% extends 'base.html' %}

{% block content %}
<div class="col-md-6 offset-md-3">
    {% if user.is_authenticated %}
        <h1>Hello Username =)</h1>
    {% else %}
        <br>
        <h1>Login</h1>
        <br>
        <form method="POST" action="{% url 'home' %}">
          {% csrf_token %}
          <div class="mb-3">
            <input type="text" class="form-control" name="username" placeholder="Username" required>
          </div>
          <div class="mb-3">
            <input type="password" class="form-control" name="password" placeholder="Password" required>
          </div>
          <button type="submit" class="btn btn-secondary">Login</button>
        </form>
    {% endif %}
</div>
{% endblock %}
```

## Registration
- URL `path('register/', views.register_user, name="register"),`
- View `def register_user(request: WSGIRequest): ...`
- Template `register.html`

## Django Forms
- create file like [`forms.py`](./crm_app/website/forms.py)
- add URL `path('register/', views.register_user, name="register"),`
- add form to views
```python
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
```
- add form to html
```html
<form method="POST" action="">
  {% csrf_token %}
    {{ form.as_p }}
  <button type="submit" class="btn btn-secondary">Register</button>
</form>
```

## Work with database
- Create model in [models.py](./crm_app/website/models.py)
```python
from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):  # it like .toString() method
        return f"{self.first_name} {self.last_name}"
```
- Now you should create migration `python manage.py makemigrations`
- Result is:
```
$ python manage.py makemigrations
Migrations for 'website':
  website\migrations\0001_initial.py
    - Create model Record
```
- And now - migrate `python manage.py migrate` it will create table `website_record`
```
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, website
Running migrations:
  Applying website.0001_initial... OK
```

- Now we need to register model `Recortd`
  - go to `admin.py`
  - import your model `from .models import Record`
  - register your model `admin.site.register(Record)`

## View records on page
- Return records from `views.py`
```python
records = Record.objects.all()
return render(request, 'home.html', {'records': records})
```
- Render Records in html
```html
  {% if records %}
      <table class="table table-striped table-hover table-bordered">
        <thead class="table-dark">
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
          </tr>
        </thead>
        <tbody>
          {% for record in records %}
          <tr>
              <td>{{ record.first_name }} {{ record.last_name }}</td>
              <td>{{ record.email }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
  {% endif %}
```

## Record page by id
- URL `path('record/<int:pk>', views.customer_record, name="record"),`
- View:
```python
def customer_record(request: WSGIRequest, pk: int):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': customer_record})
    else:
        messages.success(request, "You must been login to view this page")
        return redirect('home')
```
- Template
```html
<ul class="list-group list-group-flush">
    <li class="list-group-item">{{ record.email }}</li>
    <li class="list-group-item">{{ record.phone }}</li>
</ul>
```

## Delete record
- URL `path('delete_record/<int:pk>', views.delete_record, name="delete_record"),`
- View:
```python
def delete_record(request: WSGIRequest, pk: int):
    del_record = Record.objects.get(id=pk)
    del_record.delete()
```
- Template
- 


## Optional
[PgBouncer (connection puller)](https://www.youtube.com/watch?v=W-nOdwlxmhA)

https://youtu.be/t10QcFx7d5k?t=7265