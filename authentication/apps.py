from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration class for the authentication app.

    Handles the app's initialization and signal registration.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"

