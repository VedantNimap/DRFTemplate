from datetime import timedelta
from django.utils import timezone
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from authentication.manager import UserManager
from core.enums import LoginMethodTypeChoice


class User(AbstractUser, BaseModel):
    """
    Represents a user in the system.

    Inherits from `AbstractUser` to provide basic user functionality like passwords, permissions, and groups.
    Inherits from `TimestampModel` to automatically track creation and modification times.

    Settings:
        - `USERNAME_FIELD`: Specifies that the email field is used as the username.
        - `REQUIRED_FIELDS`: An empty list, indicating that no additional fields are required during user creation beyond the email and password.
        - `objects`: Uses the custom `UserManager` for user management.

    Meta:
        - `db_table`: Specifies the database table name for the User model.
    """
    username = None
    email = models.EmailField(unique=True,  null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    profile_picture = models.FileField(
        null=True, blank=True, upload_to="profilepictures/"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    all_objects = BaseUserManager() 

    class Meta:
        db_table = "User"

    def __str__(self):
        # Ensure it returns a non-None string
        return self.email or self.phone or "Anonymous User"


class EmailPhoneVerification(models.Model):
    email = models.EmailField(unique=True,null=True,blank=True)
    phone = models.CharField(max_length=15,unique=True,null=True,blank=True)
    otp = models.CharField(max_length=6)  # Store 6-digit OTP
    otp_expiry = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))
    is_verified = models.BooleanField(default=False)
    temp_token = models.CharField(max_length=100, null=True, blank=True)
    temp_token_expiry = models.DateTimeField(null=True, blank=True)

    def is_otp_valid(self, otp):
        """Check if OTP is valid and not expired."""
        return self.otp == otp and self.otp_expiry > timezone.now()
    
    def is_temp_token_valid(self, token):
        """Check if the temporary token is valid and not expired."""
        return self.temp_token == token and self.temp_token_expiry > timezone.now()
    
    class Meta:
        db_table = "EmailPhoneVerification"


class Session(models.Model):
    """
    Represents a user session.

    Attributes:
        - `user`: A ForeignKey to the `User` model, indicating the user associated with the session.
        - `start_time`: The timestamp when the session started.
        - `end_time`: The timestamp when the session ended.
        - `remote_address`: The IP address of the client.
        - `login_method`: The method used to log in.
        - `browser_info`: Information about the user's browser.
        - `ip_address`: The IP address of the user's device.
        - `os_info`: Information about the user's operating system.
        - `timezone`: The user's timezone.
        - `location`: User's location (optional).
        - `device_id`: A unique device identifier (optional).

    Methods:
        - `save`: Automatically sets the `end_time` to one hour after the `start_time` if it's not already set.
        - `get_local_start_time`: Returns the start time in the user's local timezone.
        - `get_local_end_time`: Returns the end time in the user's local timezone.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_sessions"
    )
    start_time = models.DateTimeField(auto_now_add=True, null=True)
    end_time = models.DateTimeField(null=True)
    remote_address = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )
    login_method_id = models.SmallIntegerField(
        db_column="login_method",
        choices=LoginMethodTypeChoice.choices,
        default=LoginMethodTypeChoice.REGULAR
    )
    browser_info = models.CharField(max_length=100, null=True, blank=True, default=None)
    ip_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    os_info = models.CharField(max_length=100, null=True, blank=True, default=None)
    timezone = models.CharField(max_length=100, null=True, blank=True, default=None)
    location = models.JSONField(null=True, blank=True, default=None)
    device_id = models.CharField(max_length=250, null=True, blank=True, default=None)

    @property
    def login_method(self):
        return self.get_login_method_id_display()

    def save(self, *args, **kwargs):
        """
        Automatically sets the end time if it's not already set.
        """
        if self.end_time is None:
            self.end_time = self.start_time + timedelta(hours=1)
        super().save(*args, **kwargs)

    def get_local_start_time(self):
        """
        Returns the start time in the user's local timezone.
        """
        return timezone.localtime(self.start_time)

    def get_local_end_time(self):
        """
        Returns the end time in the user's local timezone, or None if the end time is not set.
        """
        return timezone.localtime(self.end_time) if self.end_time else None

    class Meta:
        db_table = "Session"
