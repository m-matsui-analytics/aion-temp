import logging

# from config.logger import CustomLogger
# execute_logger = logging.getLogger("task_execute")
# error_logger = logging.getLogger("task_error")

# logger = CustomLogger()
class TaskLogger:
    """タスクエラーロガー"""

    @staticmethod
    def execute(
            # self,
            message_body: str,
            # mail_gen_log_id: [int|None],
            # job_type: [str|None],
        ) -> None:
        """
        エラーログを出力する
        """
        logging.getLogger("task_execute").info(
            "task_start",
            {
                "levelnames": "INFO",
                "message_body": message_body,
                # "mail_gen_log_id": mail_gen_log_id,
                # "job_type": job_type
            }
        )

    @staticmethod
    def error(
            # self,
            error_message: str,
            log_id: [int|None],
            job_type: [str|None]
        ) -> None:
        """
        エラーログを出力する
        """
        logging.getLogger("task_error").error(
            error_message,
            extra={
                "error_message": error_message,
                "log_id": log_id,
                "job_type": job_type
            }
        )
