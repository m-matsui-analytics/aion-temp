from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    基底アプリケーションの設定
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'


    def ready(self) -> None:  # noqa: D102
        import base.signals  # noqa: F401
