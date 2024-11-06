import logging
# execute_logger = logging.getLogger("task_execute")
# error_logger = logging.getLogger("task_error")


class APIErrorLogger:
    """タスクエラーロガー"""

    @staticmethod
    def error(
            # self,
            error_message: str,
        ) -> None:
        """
        エラーログを出力する
        """
        logging.getLogger("api_error").error(
            error_message,
            extra={
                "error_message": error_message,
            }
        )
