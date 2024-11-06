"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


import os
import urllib
from logging.handlers import TimedRotatingFileHandler  # noqa: F401
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(verbose=True)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID=1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = False
# Application definition

INSTALLED_APPS = [
    # My applications
    "api",
    "base",
    "tasks",
    "users",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # 3rd party apps
    "simple_history",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "dj_rest_auth",
    'dj_rest_auth.registration',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    "api.middlewares.LoggingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, '../api/templates'),
            os.path.join(BASE_DIR, '../templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

# User
AUTH_USER_MODEL = "users.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

OLD_PASSWORD_FIELD_ENABLED = True

DEFAULTS = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

############################################################
#  メール設定
############################################################

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

############################################################
#  タスク設定
############################################################
# JOB_TYPE_CANDIDATE_PROFILE = 1 # 候補者情報の更新
# JOB_TYPE_CAREER_DETAIL = 2 # 候補者のキャリア詳細の更新
# JOB_TYPE_IDEAL_CANDIDATE_MATCH = 3 # 求める人物像へのマッチング結果の登録
# JOB_TYPE_GEN_MAIL_OPTION = 4 # メール生成オプションの登録
# JOB_TYPE_LINK_RECRUITMENT_ARTICLE = 5 # 遷移コンテンツの登録
# JOB_TYPE_MAIL = 6 # メール登録
# JOB_TYPE_MAIL_GEN_LOG = 99 # メール作成ログの登録

############################################################
# AWS設定
############################################################
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
AWS_CLOUDWATCH_LOG_GROUP_NAME = os.getenv(
    "AWS_CLOUDWATCH_LOG_GROUP_NAME", "django-logs"
)
# SESSION = Session(region_name=AWS_REGION)
# BOTO3_CLIENT = SESSION.client("logs")



############################################################
# djangorestframework設定
############################################################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework.authentication.BasicAuthentication",
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


############################################################
# django-allauth設定
############################################################
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 認証方法をメールアドレスにする
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # Userモデルにusernameは無い
ACCOUNT_EMAIL_REQUIRED = True # メールアドレスを要求する
ACCOUNT_USERNAME_REQUIRED = False # ユーザー名を要求しない

############################################################
# Celery設定
############################################################
CELERY_TIMEZONE = "Asia/Tokyo"
# CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# BROKER_URL = "sqs://{aws_access_key}:{aws_secret_key}@".format(
#     aws_access_key=urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=''),
#     aws_secret_key=urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=''),
# )
# CELERY_BROKER_URL = "sqs://"
CELERY_BROKER_URL = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=urllib.parse.quote(AWS_ACCESS_KEY_ID, safe=''),
    aws_secret_key=urllib.parse.quote(AWS_SECRET_ACCESS_KEY, safe=''),
)

BROKER_TRANSPORT_OPTIONS = {
    'region': AWS_REGION,
    'predefined_queues': {
        # 任意のキュー名（FIFOキューの場合は.fifoをつけるが必要ある）
        'local_mail_gen_result.fifo': {
            # キューのURL
            'url': os.getenv("GENERATE_MAIL_RESULT_QUEUE_URL"),
        },
    }
}
# BROKER_TRANSPORT_OPTIONS = {
#     'region': AWS_REGION,
#     'predefined_queues': {
#         # 任意のキュー名（FIFOキューの場合は.fifoをつけるが必要ある）
#         'local_mail_gen.fifo': {
#             # キューのURL
#             'url': 'https://sqs.ap-northeast-1.amazonaws.com/024848476285/local_mail_gen.fifo',
#         },
#     }
# }
CELERY_BEAT_SCHEDULE = {
    'mail_gen_data_registerer-every-15-seconds': {
        'task': "mail_gen_data_registerer",
        'schedule': 15.0,  # 15秒ごとに実行
    },
    'content_analysis_result_registerer-every-15-seconds': {
        'task': "content_analysis_result_registerer",
        'schedule': 15.0,  # 15秒ごとに実行
    },
}

# WORKER_STATE_DB = None
# CELERY_WORKER_STATE_DB = None

# CELERY_BROKER_TRANSPORT_OPTIONS = {
#     'region': AWS_REGION,
#     'predefined_queues': {
#         # 任意のキュー名（FIFOキューの場合は.fifoをつけるが必要ある）
#         'local_mail_gen.fifo': {
#             # キューのURL
#             'url': 'https://sqs.ap-northeast-1.amazonaws.com/024848476285/local_mail_gen.fifo',
#         },
#     }
# }

# 処理が完了したらメッセージを削除する
CELERY_TASK_ACKS_LATE = True
# 例外エラーが発生したらメッセージは削除しない
CELERY_TASK_ACKS_ON_FAILURE_OR_TIMEOUT = False

# テスト時は即時実行
# CELERY_TASK_ALWAYS_EAGER = True

############################################################
# ロギング設定
############################################################

# custom_logger = CustomLogger()

# # ロギング設定を適用
# LOGGING = custom_logger.get_logging_config()
# logging.config.dictConfig(LOGGING)