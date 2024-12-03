from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'config',
    'crispy_forms',
    'crispy_bootstrap5',
    'Usuarios',
    'Cajaregistradora',
    'Inventario',
    'Proforma',
    'Facturacion',
    'Reportes',
    'Proveedores',
    'mi_aplicacion',
    'transportes',
    'geografia',
    'Orden_de_compra',
    'Clientes',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fkybsoftware',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',  # o la dirección de tu servidor PostgreSQL
        'PORT': '5432',  # el puerto por defecto de PostgreSQL es 5432
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#IPS de las cajas registradoras unidas a la red unicas
SUCURSAL_TERMINAL_CONFIG = {
    'Sucursal Central': {
        'Caja Registradora 1': '192.168.0.101',
        'Caja Registradora 2': '192.168.0.102',
    },
    'Sucursal Norte': {
        'Caja Registradora 3': '192.168.0.103',
        'Caja Registradora 4': '192.168.0.104',
    },
    'Sucursal Sur': {
        'Caja Registradora 5': '192.168.0.105',
        'Caja Registradora 6': '192.168.0.106',
    },
    'Sucursal Este': {
        'Caja Registradora 7': '192.168.0.107',
        'Caja Registradora 8': '192.168.0.108',
    },
}



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'external_login'  

#Tiempo de sesion
SESSION_COOKIE_AGE = 21600  # 6h
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

AUTH_USER_MODEL = 'Usuarios.CustomUser'

