"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url

STATUS = "staging"  #local or staging or production


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#DEFAULT_SECRET_KEY = 'iwef4uho#+p_vvc2gj=w8+cnqy1u7g4if&g_arx!02(z3!uloy'
#SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

SECRET_KEY = 'iwef4uho#+p_vvc2gj=w8+cnqy1u7g4if&g_arx!02(z3!uloy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '.example.com',  # Allow domain and subdomains
    '.example.com.',  # Also allow FQDN and subdomains
]


#BUGSNAG = {
#  "api_key": "780ff3a44e2fb9798e2319078059b5a1",
#  "project_root": "/Users/kathleenrusso/sdd_project/lh-project/mysite", #path to your app
#}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'labhelpers',       
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',#not in gettingstarted
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   # 'bugsnag.django.middleware.BugsnagMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if STATUS == "local":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', #'postgresql_psycopg2'
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#           'USER':'',
#           'PASSWORD':'',
#           'HOST':'',          # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#           'PORT':'',          # Set to empty string for default.
        }
    }
if STATUS == "staging":
    # Parse database configuration from $DATABASE_URL
    DATABASES = {   #red db
        'default': dj_database_url.config(default='postgres://veibyzxctaiutf:GR_52cvvyrOIqtfub0LBs3AgKp@ec2-54-225-255-208.compute-1.amazonaws.com:5432/d6lh4uk8nikt7g')
    }


if STATUS == "production":
    # Parse database configuration from $DATABASE_URL
    DATABASES = {   #red db
        'default': dj_database_url.config(default='postgres://qyxmyilcgnmsjr:Mk4I6FxxbQN8CfJzX5rBnupwf9@ec2-54-83-204-78.compute-1.amazonaws.com:5432/d8to2li1pmc1om')
    }

# Static asset configuration
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

#STATIC_URL = '/static/' #the url that all of static fetch in django apps will be re-routed to.

#STATIC_ROOT = 'static'  #a physical location where all of our static files will be copied to ##Or other STATIC_ROOT below 'staticfiles'

#TEMPLATE_DIRS is an iterable of the filesystem directories to check when loading Django templates; it's a search path
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]   #NOT IN OTHER FILE

TEMPLATE_LOADERS = (                                    #NOT IN OTHER FILE
    'django.template.loaders.filesystem.Loader',        #NOT IN OTHER FILE
    'django.template.loaders.app_directories.Loader',   #NOT IN OTHER FILE
)

