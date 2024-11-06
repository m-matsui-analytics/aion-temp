from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    API用アプリケーションの設定
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
