import logging
import os



from config.logger import CustomLogger

from .base import *  # noqa: F403

# load_dotenv(verbose=True)

# AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

INSTALLED_APPS += [  # noqa: F405
    "corsheaders",
    # 'puml_generator',
    # 'django_extensions',
]

MIDDLEWARE += [  # noqa: F405
    "django.middleware.common.CommonMiddleware",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True #Swagger UIでのテスト用
# CORS

############################################################
# drf_spectacular設定
############################################################

SPECTACULAR_SETTINGS = {
    'TITLE': '(ローカル)AIon 採用DX API',
    'DESCRIPTION': 'AIon 採用DX APIのローカル環境用のAPIドキュメントです。',
    'VERSION': '1.0.0',
    # 'SERVE_INCLUDE_SCHEMA': False,
    # 'SERVERS': [{'url': 'http://localhost:8000'}],
    # 'SWAGGER_UI_DIST': 'SIDECAR',
    # 'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    # 'SWAGGER_UI_SETTINGS': {
    #     'persistAuthorization': True,
    # },
    # 'REDOC_DIST': 'SIDECAR',
    # 'COMPONENT_SPLIT_REQUEST': True,
    # 'POSTPROCESSING_HOOKS': [
    #     'drf_spectacular.hooks.postprocess_schema_enums'
    # ]
}

############################################################
# ロギング設定の上書き
############################################################
custom_logger = CustomLogger()
LOGGING = custom_logger.get_logging_config()
LOGGING["loggers"]["django"]["handlers"] = ["console"]
LOGGING["loggers"]["api_request"]["handlers"] = ["console"]
LOGGING["loggers"]["api_response"]["handlers"] = ["console"]
LOGGING["loggers"]["api_error"]["handlers"] = ["console"]
LOGGING["loggers"]["task_execute"]["handlers"] = ["console"]
LOGGING["loggers"]["task_error"]["handlers"] = ["console"]

# logging.config.dictConfig(LOGGING)
# logging.
