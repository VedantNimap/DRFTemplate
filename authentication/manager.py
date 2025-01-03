from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.

    This class overrides the default `create_user` and `create_superuser` methods of BaseUserManager
    to provide custom logic for user creation and superuser creation.
    """

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        """
        Creates a new user with the given email or phone and password.

        Args:
            email (str, optional): The user's email address.
            phone (str, optional): The user's phone number.
            password (str, optional): The user's password. Defaults to None.
            extra_fields (dict, optional): Additional keyword arguments passed to the User model constructor.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If neither email nor phone is provided.
        """
        if not email and not phone:
            raise ValueError("Either email or phone must be provided.")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        """
        Creates a new superuser with the given email or phone and password.

        Ensures that the superuser has the following permissions:
            - `is_staff`: True
            - `is_superuser`: True
            - `is_active`: True
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email=email, phone=phone, password=password, **extra_fields)
    
    def create(self, **kwargs):
        return self.create_user(**kwargs)
