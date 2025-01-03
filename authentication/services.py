import random, secrets, os
from authentication.models import EmailPhoneVerification
from datetime import timedelta
from drf_template.settings import BASE_DIR
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.mail import send_mail_func
from core.sms import send_sms_func
from authentication.models import Session, User
from django.db import transaction


@transaction.atomic
def custom_login(request, response):
    """
    Handles a custom login request, validates user credentials,
    creates a session, and returns user data with permissions.

    Args:
        request (HttpRequest): The incoming login request object.
        response (HttpResponse): The response object to be modified.

    Returns:
        HttpResponse: The modified response object with user data on success,
                       or with an error message otherwise (depending on response.status_code).

    Raises:
        MultipleExceptions (e.g., PermissionError, ValidationError):
            May raise various exceptions depending on the login process.
    """
    if response.status_code == 200:
        # Login successful, proceed with user data population
        data = {
            "start_time": timezone.now(),
            "remote_address": request.META["REMOTE_ADDR"],
            "login_method_id": 1,
            "browser_info": request.data.get("browserInfo", None),
            "ip_address": request.data.get("ipAddress", None),
            "os_info": request.data.get("osInfo", None),
            "timezone": request.data.get("timezone", None),
            "location": request.data.get("location", None),
            "device_id": request.data.get("deviceId", None),
        }

        # Authenticate user based on email from request data
        user = response.data.get("user", None)

        # Create a new session object with user data and login information
        session = Session(user=user, **data)
        session.save()

        # Prepare user data with ID, email, name, groups (including permissions)
        response.data["user"] = {
            "id": user.id,
            "email": user.email,
            "phone":user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    return response


@transaction.atomic
def custom_logout(request):
    """
    Handles a custom logout request, checks for authentication,
    ends the user's session, and returns a success message.

    Args:
        request (HttpRequest): The incoming logout request object.

    Returns:
        HttpResponse: The response object containing a success message (always 200 OK).
    """

    # Check if user is already authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Successfully logged out"})

    # Get the user object from the request
    user = request.user

    # Find the latest session for the user (assuming sessions are ordered by start time)
    session = Session.objects.filter(user_id=user).order_by("-start_time").first()

    # If a session is found, update its end_time to mark it as inactive
    if session:
        session.end_time = timezone.now()
        session.save()

    # Always return a success message with status code 200 OK,
    return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)


@transaction.atomic
def extend_session_end_time(user_id):
    """
    Extends the end time of the latest session for the given user.

    Args:
        user_id (int): The ID of the user whose session to extend.
    """
    latest_session = (
        Session.objects.filter(user_id=user_id).order_by("-start_time").first()
    )
    if latest_session:
        latest_session.end_time = timezone.now() + timedelta(hours=1)
        latest_session.save()


@transaction.atomic
def generate_email_otp(email):

    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    expiry_time = timezone.now() + timedelta(minutes=5)

    # Create or update EmailVerification entry
    obj, created = EmailPhoneVerification.objects.update_or_create(
        email=email,
        defaults={"otp": otp, "otp_expiry": expiry_time, "is_verified": False},
    )
    template = os.path.join(
        BASE_DIR, "core", "templates", "otp.html"
    )  # Email template path

    # Send the OTP via email
    send_mail_func(
        to=[email],
        subject="Your OTP for Email Verification",
        template=template,
        otp=otp,
    )

    return Response({"message": "OTP sent successfully."})


@transaction.atomic
def generate_phone_otp(phone):

    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    expiry_time = timezone.now() + timedelta(minutes=5)

    # Create or update EmailVerification entry
    obj, created = EmailPhoneVerification.objects.update_or_create(
        phone=phone,
        defaults={"otp": otp, "otp_expiry": expiry_time, "is_verified": False},
    )

    # Send the OTP via email
    send_sms_func(
        phone_number=phone,
        body=f"Your OTP is {otp}",
    )

    return Response({"message": "OTP sent successfully."})


@transaction.atomic
def verify_email_otp(otp, email=None, phone=None):
    if email:
        try:
            verification = EmailPhoneVerification.objects.get(email=email)
        except EmailPhoneVerification.DoesNotExist:
            raise ValidationError({"error": "Invalid OTP."})
    elif phone:
        try:
            verification = EmailPhoneVerification.objects.get(phone=phone)
        except EmailPhoneVerification.DoesNotExist:
            raise ValidationError({"error": "Invalid OTP or phone number."})
    else:
        raise ValidationError({"error": "Either email or phone must be provided."})

    if not verification.is_otp_valid(otp):
        raise ValidationError({"error": "Invalid or expired OTP."})

    # Mark the email as verified
    # verification.is_verified = True
    verification.save()

    # Generate a temporary token
    temp_token = secrets.token_urlsafe(32)

    # Store the token in the database
    verification.temp_token = temp_token
    verification.temp_token_expiry = timezone.now() + timedelta(minutes=10)
    verification.save()

    return Response({"message": "Email verified successfully.", "token": temp_token})


@transaction.atomic
def validate_and_register_user(validated_data, token):
    """
    Validates the email verification token and processes user registration.

    Args:
        validated_data (dict): The validated data from the serializer.
        token (str): The temporary token from the request headers.

    Raises:
        ValidationError: If the email is not verified or the token is invalid.
    """
    email = validated_data.get("email", None)
    phone = validated_data.get("phone", None)

    try:
        if email:
            verification = EmailPhoneVerification.objects.get(email=email)
        elif phone:
            verification = EmailPhoneVerification.objects.get(phone=phone)

        # Check if the token is valid
        if not verification.is_temp_token_valid(token):
            raise ValidationError({"token": "Invalid or expired token."})
    except EmailPhoneVerification.DoesNotExist:
        raise ValidationError(
            {"detail": "Verification record not found for the provided email/phone."}
        )

    # Optionally, clean up the token
    verification.temp_token = None
    verification.save()
