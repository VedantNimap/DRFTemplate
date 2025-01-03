from django.db.models import Min
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from core.mixins import PublicAPIMixin
from master.serializers import StatusCodeSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authentication import api_descriptions, serializers, services, models


@extend_schema(description=api_descriptions.CUSTOM_JWT_LOGIN_DESCRIPTION)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Customizes the token obtain pair view to handle custom login logic.

    Inherits from `TokenObtainPairView` to provide base functionality for obtaining access tokens.
    Uses a custom serializer `CustomTokenObtainPairSerializer` for additional validation and data processing.
    Overrides the `post` method to call the `custom_login` service, which likely handles:
        - Session creation
        - User data updates
        - Custom claim addition to the token
        - Response modification
    """

    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to obtain a token.

        Calls the parent class's `post` method to get the initial response.
        Passes the request and response to the `custom_login` service for further processing.
        Returns the modified response from the service.
        """
        response = super().post(request, *args, **kwargs)
        return services.custom_login(request, response)


@extend_schema(description=api_descriptions.CUSTOM_LOGOUT_DESCRIPTION)
class CustomLogoutView(ListAPIView):
    """
    View for handling user logout.

    Inherits from `ListAPIView` to leverage its basic structure, although we don't use the queryset or typical list operations.
    Uses `StatusCodeSerializer` to return a simple status code response.
    Requires authentication (`IsAuthenticated` permission class).
    """

    queryset = []
    permission_classes = [IsAuthenticated]
    serializer_class = StatusCodeSerializer

    def list(self, request, *args, **kwargs):
        """
        Handles the GET request for logout.

        Calls the `services.custom_logout` function to perform logout actions, which likely:
            - Invalidates tokens
            - Clears session data
            - Potentially logs the logout event
        Returns the response from the `services.custom_logout` function, which typically indicates success or failure.
        """

        return services.custom_logout(request)


@extend_schema(description=api_descriptions.TOKEN_VERIFY_DESCRIPTION)
class CustomTokenVerifyView(TokenVerifyView):
    """
    Customizes the token verification view.

    Inherits from `TokenVerifyView` to provide base functionality for verifying tokens.
    Extends the base behavior by potentially adding custom logic in subclasses or overriding methods.
    """

    pass


@extend_schema(description=api_descriptions.TOKEN_REFRESH_DESCRIPTION)
class CustomTokenRefreshView(TokenRefreshView):
    """
    Customizes the token refresh view.

    Inherits from `TokenRefreshView` to provide base functionality for refreshing access tokens.
    Extends the behavior by adding logic to potentially extend session end time upon successful refresh.
    """

    def post(self, request, *args, **kwargs):
        """
        Processes POST requests to refresh access tokens.

        Calls the parent class's `post` method to handle the base token refresh logic.
        - This likely retrieves the refresh token from the request data, validates it,
          and generates a new access token pair.

        Checks the response status code (200 indicates successful refresh).
        If refresh is successful:

            - Extracts the user ID from the decoded refresh token using `RefreshToken`.

            - Calls `services.extend_session_end_time(user_id)` to potentially extend the session
              end time for the user (implementation details in `services`).

            - Catches exceptions (e.g., invalid token) but doesn't explicitly handle them.

        Returns the response from the parent class (containing the new access token pair).
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Decode the refresh token to get the user ID
            refresh_token = request.data.get("refresh")
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    user_id = token["user_id"]
                    services.extend_session_end_time(user_id)
                except Exception as e:
                    # Handle exceptions (e.g., invalid token)
                    pass

        return response


class GenerateEmailOTPAPIView(PublicAPIMixin, CreateAPIView):
    """
    API for generating OTP for email verification.
    """

    serializer_class = serializers.EmailVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.generate_otp()

class GeneratePhoneOTPAPIView(PublicAPIMixin, CreateAPIView):
    """
    API for generating OTP for phone verification.
    """

    serializer_class = serializers.PhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.generate_otp()



class VerifyOTPAPIView(PublicAPIMixin, CreateAPIView):
    serializer_class = serializers.OTPVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.verify_otp()
    

class UserRegistrationAPIView(PublicAPIMixin, CreateAPIView):
    """
    User registration API. This endpoint should be used to allow
    new registration.
    """

    serializer_class = serializers.UserCreateSerializer

    def perform_create(self, serializer):
        # Delegate the validation logic to the service layer
        services.validate_and_register_user(
            serializer.validated_data, self.request.headers.get("Authorization")
        )
        serializer.save()


@extend_schema(description=api_descriptions.PROFILE_LIST_DESCRIPTION)
class ProfileListAPIView(ListAPIView):
    """
    View for retrieving a user's profile information.

    Inherits from `ListAPIView` to leverage its functionality for retrieving and listing data.
    Sets `serializer_class` to `serializers.UserSerializer` to serialize the user data.
    Requires authentication (`IsAuthenticated` permission class).
    Disables pagination (`pagination_class = None`) as we only expect a single user profile.
    """

    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """
        Customizes the queryset to retrieve only the current user's profile.

        Filters users by ID to match the currently authenticated user's ID (`self.request.user.id`).
        Selects related data from the "person_details" field using `select_related`.

        Returns the queryset containing the user profile information.
        """
        return models.User.objects.filter(id=self.request.user.id)


@extend_schema_view(
    patch=extend_schema(
        description=api_descriptions.PROFILE_PICTURE_UPDATE_DESCRIPTION,
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "profile_picture": {
                        "type": "string",
                        "format": "binary",
                        "description": "Profile picture file to upload",
                    }
                },
                "required": ["profile_picture"],
            }
        },
    ),
    put=extend_schema(
        description=api_descriptions.PROFILE_PICTURE_UPDATE_DESCRIPTION,
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "profile_picture": {
                        "type": "string",
                        "format": "binary",
                        "description": "Profile picture file to upload",
                    }
                },
                "required": ["profile_picture"],
            }
        },
    ),
)
class ProfilePictureUpdateAPIView(UpdateAPIView):
    """
    View for updating a user's profile picture.

    Inherits from `UpdateAPIView` to handle updates to model instances.
    Requires authentication (`IsAuthenticated` permission class).
    Uses `serializers.ProfilePictureSerializer` to validate and serialize profile picture data.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfilePictureSerializer

    def get_object(self):
        return self.request.user


@extend_schema(description=api_descriptions.RECENT_ACTIVITY_LIST_DESCRIPTION)
class RecentActivityListAPIView(ListAPIView):
    """
    View for retrieving a user's recent activity (login sessions).

    Inherits from `ListAPIView` to leverage its functionality for retrieving and listing data.
    Sets `serializer_class` to `serializers.SessionSerializer` to serialize session data.

    """

    serializer_class = serializers.SessionSerializer

    def get_queryset(self):
        """
        Customizes the queryset to retrieve the current user's recent login sessions.
        Filters sessions by user ID to match the currently authenticated user's ID (`self.request.user.id`).
        Selects related data from the "user" field using `select_related`.
        Orders sessions by start time in descending order (`-start_time`) to show the most recent first.
        Returns the queryset containing the user's recent login sessions.
        """

        queryset = (
            models.Session.objects.select_related("user")
            .filter(user_id=self.request.user.id)
            .order_by("-start_time")
        )
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Processes the request, retrieves sessions, and adds additional data to the response.
        Calls the parent class's `list` method to retrieve the list of sessions using the custom queryset.
        Extracts the current user's ID from the request.
        Calculates the number of distinct devices used for logins:
            - Filters sessions for the current user with non-null device IDs (`device_id__isnull=False`).
            - Uses `.values("device_id")` to select only the "device_id" field.
            - Applies `.distinct()` to remove duplicates.
            - Counts the number of distinct devices using `.count()`.
        Finds the time of the first login:
            - Filters sessions for the current user.
            - Uses `.aggregate(first_login=Min("start_time"))` to get the minimum start time.
            - Extracts the "first_login" value from the aggregated result.
        Adds the calculated data ("distinct_device_count" and "first_login") to the response data.
        Returns the modified response object.
        """

        response = super().list(request, *args, **kwargs)
        user_id = self.request.user.id
        distinct_devices_count = (
            models.Session.objects.filter(user_id=user_id, device_id__isnull=False)
            .values("device_id")
            .distinct()
            .count()
        )

        first_login = (
            models.Session.objects.filter(user_id=user_id).aggregate(
                first_login=Min("start_time")
            )
        )["first_login"]

        response.data["distinct_device_count"] = distinct_devices_count
        response.data["first_login"] = first_login
        return response
