import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + '\n')

SERVICES = {
    'customer_service': {
        'type': 'portal',
        'app': 'customer_app',
        'db_url': 'mysql://root:rootpassword@db_customer:3306/customer_db'
    },
    'staff_service': {
        'type': 'portal',
        'app': 'staff_app',
        'db_url': 'mysql://root:rootpassword@db_staff:3306/staff_db'
    },
    'laptop_service': {
        'type': 'catalog',
        'app': 'laptop_app',
        'db_url': 'postgres://user:password@db_laptop:5432/laptop_db'
    },
    'mobile_service': {
        'type': 'catalog',
        'app': 'mobile_app',
        'db_url': 'postgres://user:password@db_mobile:5432/mobile_db'
    }
}

REQUIREMENTS = """
Django==4.2.11
djangorestframework==3.15.1
dj-database-url==2.1.0
psycopg2-binary==2.9.9
pymysql==1.1.0
requests==2.31.0
django-cors-headers==4.3.1
"""

for service_name, config in SERVICES.items():
    proj = config['type']
    app = config['app']
    
    # requirements.txt
    write_file(f"{service_name}/requirements.txt", REQUIREMENTS)
    
    # Dockerfile
    dockerfile = f"""
FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/{proj}
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
"""
    write_file(f"{service_name}/Dockerfile", dockerfile)
    
    # manage.py
    manage = f"""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{proj}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""
    write_file(f"{service_name}/{proj}/manage.py", manage)
    
    # settings.py
    settings = f"""
import os
import dj_database_url
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dummy'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    '{app}',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{proj}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{proj}.wsgi.application'

DATABASES = {{
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
"""
    write_file(f"{service_name}/{proj}/{proj}/__init__.py", "")
    write_file(f"{service_name}/{proj}/{proj}/settings.py", settings)
    
    # urls.py
    urls = f"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('{app}.urls')),
]
"""
    write_file(f"{service_name}/{proj}/{proj}/urls.py", urls)
    
    # wsgi.py
    wsgi = f"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{proj}.settings')
application = get_wsgi_application()
"""
    write_file(f"{service_name}/{proj}/{proj}/wsgi.py", wsgi)
    
    # app
    write_file(f"{service_name}/{proj}/{app}/__init__.py", "")
    write_file(f"{service_name}/{proj}/{app}/admin.py", "from django.contrib import admin")
    write_file(f"{service_name}/{proj}/{app}/apps.py", f"from django.apps import AppConfig\n\nclass {app.title().replace('_', '')}Config(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = '{app}'")
    write_file(f"{service_name}/{proj}/{app}/views.py", "from rest_framework import viewsets")
    write_file(f"{service_name}/{proj}/{app}/models.py", "from django.db import models")
    write_file(f"{service_name}/{proj}/{app}/serializers.py", "from rest_framework import serializers")
    write_file(f"{service_name}/{proj}/{app}/urls.py", f"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
""")

print("Django projects scaffolded.")
