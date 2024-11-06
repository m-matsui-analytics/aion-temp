import os
from django.utils import timezone

# import logging
import boto3
from datetime import datetime
from dotenv import load_dotenv
from zoneinfo import ZoneInfo


load_dotenv()

AWS_CLOUDWATCH_LOG_GROUP_NAME = os.getenv("AWS_CLOUDWATCH_LOG_GROUP_NAME")

class CustomLogger:
    """
    ロギング設定を管理するクラス
    """

    # api_format = """%(asctime)s %(created)f %(method)s %(endpoint)s %(status_code)s
    #                 %(user_id)s %(request_ip)s %(user_agent)s %(request_params)s %(response_time_ms)s
    #                 %(host)s %(request_id)s"""

    def __init__(self) -> None:  # noqa: D10
        aws_region = os.getenv("AWS_REGION", "ap-northeast-1")
        self.boto3_logs_client = boto3.client("logs", region_name=aws_region)
        self.today = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%Y-%m-%d')

    # @staticmethod
    # def get_log_log_stream_name() -> str:
    #     """
    #     現在の日付を基にログファイル名を生成
    #     """
    #     current_time = timezone.now()
    #     return f"django-log-{current_time.strftime('%Y%m%d')}"

    def get_logging_config(self) -> dict:
        """
        ロギング設定を取得
        """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "fmt": "{levelname} {asctime} {module} {message}",
                    "style": "{",
                },
                "simple": {
                    "fmt": "{levelname} {message}",
                    "style": "{",
                },
                "api_request": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": """
                        %(asctime)s %(created)f %(method)s %(endpoint)s
                        %(user_id)s %(request_ip)s %(user_agent)s %(request_params)s
                        %(host)s %(request_id)s
                    """,
                },
                "api_response": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": """
                        %(asctime)s %(created)f %(status_code)s %(run_time_ms)s
                        %(response_body)s %(request_id)s
                    """,
                },
                "api_error": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(asctime)s %(created)f %(error_message)s %(request_id)s",
                },
                "task_execute": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(levelnames)s %(asctime)s %(created)f %(message_body)s",
                },
                "task_error": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": """
                        %(asctime)s %(created)f %(levelname)s %(funcName)s
                        %(log_id)s %(job_type)s %(error_message)s
                    """,
                },
            },
            "handlers": {
                "cloudwatch_api_request_log": {
                    "level": "INFO",
                    "class": "watchtower.CloudWatchLogHandler",
                    "boto3_client": self.boto3_logs_client,
                    "log_group_name": AWS_CLOUDWATCH_LOG_GROUP_NAME,
                    "log_stream_name": f"{self.today}-api-request.log",
                    "formatter": "api_request",
                },
                "cloudwatch_api_response_log": {
                    "level": "INFO",
                    "class": "watchtower.CloudWatchLogHandler",
                    "boto3_client": self.boto3_logs_client,
                    "log_group_name": AWS_CLOUDWATCH_LOG_GROUP_NAME,
                    "log_stream_name": f"{self.today}-api-response.log",
                    "formatter": "api_response",
                },
                "cloudwatch_api_error_log": {
                    "level": "ERROR",
                    "class": "watchtower.CloudWatchLogHandler",
                    "boto3_client": self.boto3_logs_client,
                    "log_group_name": AWS_CLOUDWATCH_LOG_GROUP_NAME,
                    "log_stream_name": f"{self.today}-api-error.log",
                    "formatter": "api_error",
                },
                "cloudwatch_api_task_execute_log": {
                    "level": "INFO",
                    "class": "watchtower.CloudWatchLogHandler",
                    "boto3_client": self.boto3_logs_client,
                    "log_group_name": AWS_CLOUDWATCH_LOG_GROUP_NAME,
                    "log_stream_name": f"{self.today}-task-execute.log",
                    "formatter": "task_execute",
                },
                # CloudWatchへのハンドラー（タスクエラーログ用）
                "cloudwatch_task_error_log": {
                    "level": "ERROR",
                    "class": "watchtower.CloudWatchLogHandler",
                    "boto3_client": self.boto3_logs_client,
                    "log_group_name": AWS_CLOUDWATCH_LOG_GROUP_NAME,
                    "log_stream_name": f"{self.today}-task-error.log",
                    "formatter": "task_error",
                },
                "console_api_request_log": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "api_request",
                },
                "console_api_response_log": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "api_response",
                },
                "console_api_error_log": {
                    "level": "ERROR",
                    "class": "logging.StreamHandler",
                    "formatter": "api_error",
                },
                "console_api_task_execute_log": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "task_execute",
                },
                "console_task_error_log": {
                    "level": "ERROR",
                    "class": "logging.StreamHandler",
                    "formatter": "task_error",
                },
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },
            },
            "loggers": {
                "django": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": True,
                },
                "api_request": {
                    "handlers": ["cloudwatch_api_request_log"],
                    "level": "INFO",
                    "propagate": False,
                },
                "api_response": {
                    "handlers": ["cloudwatch_api_response_log"],
                    "level": "INFO",
                    "propagate": False,
                },
                "api_error": {
                    "handlers": ["cloudwatch_api_error_log"],
                    "level": "ERROR",
                    "propagate": False,
                },
                "task_execute": {
                    "handlers": ["cloudwatch_task_execute_log"],
                    "level": "INFO",
                    "propagate": False,
                },
                "task_error": {
                    "handlers": ["cloudwatch_task_error_log"],
                    "level": "ERROR",
                    "propagate": False,
                },
            },
        }
