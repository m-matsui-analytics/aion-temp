from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from api.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
    UserSerializer,
)
from api.views.mixins import with_error_responses
from api.views.responses import NotFoundResponse
from users.models import CustomUser as User


@with_error_responses('get')
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.PATH,
            required=True,
            description="ユーザーID"
        )
    ]
)
class UserView(RetrieveAPIView):
    """
    ユーザーモデルのビュー
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        """
        ユーザー情報の取得
        """
        user_id = request.headers.get('UserID')
        user = self.get_queryset().filter(id=user_id).first()
        if not user:
            return NotFoundResponse("user")

        serializer = self.serializer_class(user)
        return Response(serializer.data)


#####################################################################
# djangorestframework-simplejwtのカスタム
#####################################################################
class CustomTokenObtainPairView(TokenObtainPairView):  # noqa: D101
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):  # noqa: D101
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenVerifyView(TokenVerifyView):  # noqa: D101
    serializer_class = CustomTokenVerifySerializer
