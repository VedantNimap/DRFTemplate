from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from authentication import helpers, models, services
from authentication.models import Session, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):


    browserInfo = serializers.CharField(required=False, write_only=True)
    ipAddress = serializers.CharField(required=False, write_only=True)
    osInfo = serializers.CharField(required=False, write_only=True)
    timezone = serializers.CharField(required=False, write_only=True)
    location = serializers.JSONField(required=False, write_only=True)
    deviceId = serializers.CharField(required=False, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # Extract email/phone and password from the request
        username = attrs.get("email", None)
        password = attrs.get("password", None)

        # Check if the username is email or phone
        user = None
        if "@" in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(phone=username).first()
        
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid login credentials.")

         # Use the email or phone as the username_field value
        username_value = user.email if user.email else user.phone


        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        # Include additional user details in the response
        data["user"] = user

        return data


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def generate_otp(self):
        """Helper function to call the service function."""
        return services.generate_email_otp(self.validated_data["email"])


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()

    def generate_otp(self):
        """Helper function to call the service function."""
        return services.generate_phone_otp(self.validated_data["phone"])


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)


    def validate(self, attrs):
        helpers.validate_email_or_phone_exist(attrs)
        return attrs

    def verify_otp(self):
        email = self.validated_data.get("email", None)
        phone = self.validated_data.get("phone", None)
        return services.verify_email_otp(
            otp=self.validated_data["otp"], email=email, phone=phone
        )


class ConfirmPasswordInMixin(serializers.Serializer):
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data = helpers.validate_confirm_password(attrs)
        return validated_data


class UserCreateSerializer(ConfirmPasswordInMixin, serializers.ModelSerializer):
    """
    Serializer for `User Registration` API
    """

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "confirm_password",
            "profile_picture",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "profile_picture": {"required": False},
            "email": {"required": False},
            "phone": {"required": False},
        }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data = helpers.validate_email_or_phone_exist(attrs)
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Inherits from `serializers.ModelSerializer` to automatically handle serialization and deserialization of model fields.

    Fields:
        - `id`: The unique identifier of the user.
        - `email`: The user's email address.
        - `first_name`: The user's first name.
        - `last_name`: The user's last name.
        - `profile_picture`: The user's profile picture URL or file path.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
        ]


class ProfilePictureSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a user's profile picture.

    Inherits from `serializers.ModelSerializer` to provide a foundation for serialization and deserialization.
    Focuses specifically on the `profile_picture` field of the `User` model.

    Fields:
        - `profile_picture`: The user's profile picture.

    update method:
        - Overridden to handle updating the user's profile picture.
        - Extracts the `profile_picture` field from the validated data.
        - If the field is present, updates the user's profile_picture attribute.
        - Otherwise, keeps the existing picture.
        - Saves the updated user instance.
        - Returns the updated user instance.
    """

    class Meta:
        model = User
        fields = ["profile_picture"]

    def update(self, instance, validated_data):
        """
        Updates the user's profile picture based on the provided data.

        Args:
            instance: The user object to be updated.
            validated_data: The validated data from the serializer.

        Returns:
            The updated user instance.
        """

        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.save()
        return instance


class SessionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Session model.

    Inherits from `serializers.ModelSerializer` to automatically handle serialization and deserialization of all model fields.
    """

    class Meta:
        model = Session
        fields = [
            "id",
            "start_time",
            "end_time",
            "remote_address",
            "login_method",
            "browser_info",
            "ip_address",
            "os_info",
            "timezone",
            "location",
            "device_id",
        ]
