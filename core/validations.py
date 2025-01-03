from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException,_get_error_details


class CustomValidationError(APIException):
    """
    Custom exception class for handling validation errors in APIs.
    Extends DRF's `APIException` to allow for flexible error reporting with 
    enhanced customization.

    Attributes:
        status_code (int): HTTP status code for the response. Defaults to 400 (Bad Request).
        default_detail (str): Default error message if no detail is provided.
        default_code (str): Default error code if no specific code is provided.
    """

    status_code = status.HTTP_400_BAD_REQUEST  # Sets the HTTP status code for the exception.
    default_detail = _("Invalid input.")  # Default error message, translatable for i18n.
    default_code = "invalid"  # Default error code for the exception.

    def __init__(self, detail=None, code=None):
        """
        Initialize the exception with custom detail and code.

        Args:
            detail (str, dict, or list, optional): Custom error message or data.
                                                   Defaults to `default_detail` if not provided.
            code (str, optional): Custom error code. Defaults to `default_code`.
        """

        # Use the default detail if none is provided.
        if detail is None:
            detail = self.default_detail
        
        # Use the default code if none is provided.
        if code is None:
            code = self.default_code

        # Ensure the detail is formatted as a list or dictionary for consistency.
        # Single strings or other types are not converted into complex structures.
        if isinstance(detail, tuple):  # Handles cases where detail might be a tuple.
            detail = detail
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = detail

        # Leverages DRF's internal method for consistent error structure.
        self.detail = _get_error_details(detail, code)