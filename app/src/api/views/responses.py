import logging

from rest_framework import status
from rest_framework.response import Response


class NotFoundResponse(Response):
    """
    値が見つからない場合のレスポンス
    """

    def __init__(self, item_name: str) -> None:  # noqa: D107
        super().__init__({f"detail: {item_name}"}, status=status.HTTP_404_NOT_FOUND)

class SuccessResponse(Response):
    """
    成功時のレスポンス
    """

    def __init__(self,) -> None:  # noqa: D107
        super().__init__({}, status=status.HTTP_200_OK)

        # アクセスログを出力
        logger = logging.getLogger("api_request")



class FailureResponse(Response):
    """
    エラーレスポンス
    """

    def __init__(self, message: str) -> None:  # noqa: D107
        super().__init__({f"detail: {message}"}, status=status.HTTP_400_BAD_REQUEST)

class TypeErrorResponse(Response):
    """型エラーの場合のエラーレスポンス"""

    def __init__(self, item_name: str) -> None:  # noqa: D107
        super().__init__({f"TypeError: [{item_name}]"}, status=status.HTTP_400_BAD_REQUEST)

class PathParamErrorResponse(Response):
    """パスパラメータが指定されていないときのエラーレスポンス"""

    def __init__(self, item_name: str) -> None:  # noqa: D107
        super().__init__({f"PathParamErrorResponse: [{item_name}]"}, status=status.HTTP_400_BAD_REQUEST)
