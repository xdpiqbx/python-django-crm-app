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

## Optional
[PgBouncer (connection puller)](https://www.youtube.com/watch?v=W-nOdwlxmhA)

https://youtu.be/t10QcFx7d5k?t=1730