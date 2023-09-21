from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response:
        error_type = type(exc).__name__

        if hasattr(exc, 'error_data'):
            response_body_data = exc.error_data
        else:
            response_body_data = str(exc)
        
        error_detail = f"{error_type}({response_body_data})"

        response = Response(
            data={'detail': error_detail},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response