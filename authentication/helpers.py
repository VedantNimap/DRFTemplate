from rest_framework.serializers import ValidationError


def validate_confirm_password(data):
    """
    Validates that the 'password' and 'confirm_password' fields in the input data match.

    Args:
        data (dict): A dictionary containing the fields 'password' and 'confirm_password'.

    Raises:
        ValidationError: If the 'password' and 'confirm_password' fields do not match.

    Returns:
        dict: The input data with the 'confirm_password' field removed if validation passes.
    
    Notes:
        - This function is typically used in serializers or forms where both 'password'
          and 'confirm_password' fields are provided to ensure they match before processing.
        - The 'confirm_password' field is removed from the data to prevent storing it or
          further processing.
    """
    
    if data.get("password") != data.get("confirm_password"):
        raise ValidationError(
            {"password": "Password and Confirm Password do not match."}
        )
    data.pop("confirm_password")
    return data

def validate_email_or_phone_exist(data):
    email = data.get("email")
    phone = data.get("phone")

    # Ensure either email or phone is provided, but not both
    if not email and not phone:
        raise ValidationError("Either email or phone must be provided.")
    if email and phone:
        raise ValidationError(
            "Provide only one of email or phone, not both."
        )

    return data

