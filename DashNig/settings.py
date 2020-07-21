import os
import dj_database_url
import django_heroku


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']


DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  "post_office",
  'BeginningDash',

  #Third party Apps
  'crispy_forms',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.gzip.GZipMiddleware",
    'DashNig.middleware.LoginRequiredMiddleware',
]


CRISPY_TEMPLATE_PACK = 'bootstrap3'
ROOT_URLCONF = 'DashNig.urls'

TEMPLATES = [
    {
      'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': [ os.path.join(BASE_DIR, 'templates')],
      'APP_DIRS': True,
      'OPTIONS': {
          'context_processors': [
              'django.template.context_processors.debug',
              'django.template.context_processors.request',
              'django.contrib.auth.context_processors.auth',
              'django.contrib.messages.context_processors.messages',
              'BeginningDash.context_processors.status',
              'BeginningDash.context_processors.newscount',      
              'BeginningDash.context_processors.statistics',
              'BeginningDash.context_processors.statistics_4_code',
              'BeginningDash.context_processors.say_sth',   
          ],
      },
    },
]

WSGI_APPLICATION = 'DashNig.wsgi.application'


DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587



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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/home/dashboard/'


LOGIN_URL = '/login-reg/'

LOGIN_EXEMPT_URLS = (
  r'^account/logout/$',
  r'^login-reg/',
  r'^register/',
  r'^aboutfornonuser/',
  r'^mycontact4offlineuser/',
  r'^change-password/$',
  r'^reset-password/$',
  r'^reset-password/done/$',
  r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
  r'^reset-password/complete/$',
)



# For production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')