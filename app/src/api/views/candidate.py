from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.candidate import CandidateSerializer
from api.views.mixins import (
    with_error_responses,
    # with_get_error_responses,
    # with_put_error_responses,
)
from base.models import Candidate


class CandidateView(views.APIView):
    """
    会社概要のビュー
    """

    @with_error_responses('get')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="UserID",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.HEADER,
                required=True,
                description="ユーザーID"
            ),
            OpenApiParameter(
                name="Authorization",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                required=True,
                description="JWTトークン"
            )
        ]
    )

    # def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
    #     """取得"""
    #     candidate_id = request.candidate.id

    #     candidate = get_object_or_404(
    #         Candidate,
    #         id=candidate_id,
    #         deleted_at=None
    #     )

    #     serializer = CandidateSerializer(instance=candidate)

    #     return Response(serializer.data)

    @with_error_responses('put')
    @extend_schema(
        # parameters=candidate_info_parameters
        request=CandidateSerializer,
    )
    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """更新"""
        candidate_id = request.id
        candidate = get_object_or_404(
            Candidate,
            id=candidate_id,
        )

        serializer = CandidateSerializer(
            instance=candidate,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

