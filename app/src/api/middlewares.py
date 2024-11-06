import logging
import time
import uuid

from rest_framework import status
from rest_framework.response import Response


class LoggingMiddleware:
    """
    APIアクセスログを出力するミドルウェア
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = None

        try:
            # リクエストIDを生成してリクエストオブジェクトに保存
            request.id = str(uuid.uuid4())
            # 管理画面へのアクセスの場合はログを記録しない
            if request.path.startswith('/api/'):
                self.log_request(request)
                response = self.get_response(request)
                self.log_response(request, response, start_time)
            else:
                response = self.get_response(request)
        except Exception as e:
            # エラーログを出力（ここで検知できるエラーはリクエスト・レスポンスの処理に関するエラーのみ）
            print("execute error logging")
            self.log_error(request, e)
            response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    def log_request(self, request):
        request_logger = logging.getLogger("api_request")
        log_data = {
            "method": request.method,
            "endpoint": request.path,
            "user_id": getattr(request, "user", None),
            # "user_id": getattr(request.user, "id", None),
            "request_ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "request_params": request.GET.dict() if request.method == "GET" else request.POST.dict(),
            "host": request.get_host(),
            "request_id": request.id,
        }
        request_logger.info(log_data)

    def log_response(self, request, response, start_time):
        response_logger = logging.getLogger("api_response")
        log_data = {
            "status_code": response.status_code,
            "run_time_ms": int((time.time() - start_time) * 1000),
            "response_body": getattr(response, "data", {}),
            "request_id": request.id,
        }
        response_logger.info(log_data)

    def log_error(self, request, exception):
        error_logger = logging.getLogger("api_error")
        log_data = {
            "request_id": request.id,
            "error_message": str(exception)
        }
        error_logger.error(log_data)
