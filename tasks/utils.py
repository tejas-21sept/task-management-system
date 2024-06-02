from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_response(data=None, message="", code=status.HTTP_200_OK, errors=None):
    response = {
        "code": code,
        "message": message,
        "data": data,
        "errors": errors,
    }
    return Response(response, status=code)


# Custom exception handler to use the standardized error response structure
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = [
            {"field": key, "message": value} for key, value in response.data.items()
        ]
        response.data = {
            "code": response.status_code,
            "message": "An error occurred",
            "data": None,
            "errors": errors,
        }

    return response
