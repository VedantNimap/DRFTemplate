from django.db import models


class LoginMethodTypeChoice(models.IntegerChoices):
    """
    Enumeration of login methods for user authentication.
    """
    
    REGULAR = 1, "REGULAR"
    GOOGLE = 2, "GOOGLE"