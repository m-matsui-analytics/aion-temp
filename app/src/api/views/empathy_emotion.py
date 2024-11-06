from typing import ClassVar

from rest_framework import status, views
from rest_framework.request import Request
from rest_framework.response import Response

from api.permissions import IsBuilderUser
from base.models import EmpathyEmotion


class EmpathyEmotionView(views.APIView):
    """
    選択肢: 共感する感情のビュー
    """

    permission_classes: ClassVar = [IsBuilderUser,]

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """取得"""
        choices = [{"value": choice.value, "label": choice.label} for choice in EmpathyEmotion]  # noqa: E501
        return Response(choices, status=status.HTTP_200_OK)
