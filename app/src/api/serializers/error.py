from rest_framework import serializers


# 404用のカスタムレスポンスシリアライザを定義
class ErrorResponseSerializer(serializers.Serializer):
    """
    エラーレスポンスのシリアライザ
    """

    detail = serializers.CharField()


# class CustomValidationError(serializers.ErrorDetail):
#     """
#     バリデーションエラーの例外クラス
#     """

#     def __init__(self, : str) -> None:
#         super().__init__(detail=detail)
