from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.views import APIView

from api.serializers.error import ErrorResponseSerializer


def with_error_responses(method):
    """
    Add error responses (400, 401, 403, 404) to a view method for Swagger UI.

    :param method: The HTTP method (e.g., 'get', 'post', 'put') to which the common error responses will be added.
    :return: A decorator function that adds common error responses to the specified method.
    """
    def decorator(func):
        return extend_schema(
            responses={
                400: OpenApiResponse(description="Bad Request"),
                401: OpenApiResponse(description="Unauthorized"),
                403: OpenApiResponse(description="Forbidden"),
                404: OpenApiResponse(ErrorResponseSerializer, description="Not Found"),
            }
        )(func)
    return decorator

# Usage examples:
# @with_error_responses('get')
# @with_error_responses('post')
# @with_error_responses('put')

# # mixins.py
# from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
# from rest_framework.views import APIView

# from api.serializers.error import ErrorResponseSerializer


# def with_get_error_responses(view_class: type[APIView]) -> type[APIView]:
#     """
#     Add GET error responses (400, 401, 403, 404) to a view class for Swagger UI.

#     :param view_class: The view class to which the common error responses will be added.
#     :return: The modified view class with common error responses.
#     """
#     return extend_schema_view(
#         get=extend_schema(
#             responses={
#                 400: OpenApiResponse(
#                     description="Bad Request"
#                 ),
#                 401: OpenApiResponse(
#                     description="Unauthorized"
#                 ),
#                 403: OpenApiResponse(
#                     description="Forbidden"
#                 ),
#                 404: OpenApiResponse(
#                     ErrorResponseSerializer,
#                     description="Not Found"
#                 ),
#             }
#         ),
#     )(view_class)

# def with_post_error_responses(view_class: type[APIView]) -> type[APIView]:
#     """
#     Add GET error responses (400, 401, 403, 404) to a view class for Swagger UI.

#     :param view_class: The view class to which the common error responses will be added.
#     :return: The modified view class with common error responses.
#     """
#     return extend_schema_view(
#         post=extend_schema(
#             responses={
#                 400: OpenApiResponse(
#                     description="Bad Request"
#                 ),
#                 401: OpenApiResponse(
#                     description="Unauthorized"
#                 ),
#                 403: OpenApiResponse(
#                     description="Forbidden"
#                 ),
#                 404: OpenApiResponse(
#                     ErrorResponseSerializer,
#                     description="Not Found"
#                 ),
#             }
#         ),
#     )(view_class)

# def with_put_error_responses(view_class: type[APIView]) -> type[APIView]:
#     """
#     Add GET error responses (400, 401, 403, 404) to a view class for Swagger UI.

#     :param view_class: The view class to which the common error responses will be added.
#     :return: The modified view class with common error responses.
#     """
#     return extend_schema_view(
#         put=extend_schema(
#             responses={
#                 400: OpenApiResponse(
#                     description="Bad Request"
#                 ),
#                 401: OpenApiResponse(
#                     description="Unauthorized"
#                 ),
#                 403: OpenApiResponse(
#                     description="Forbidden"
#                 ),
#                 404: OpenApiResponse(
#                     ErrorResponseSerializer,
#                     description="Not Found"
#                 ),
#             }
#         ),
#     )(view_class)

