from django.db import models
from softdelete.models import SoftDeleteModel

class TimestampModel(models.Model):
    """
    Abstract base model to add timestamp fields (`created_at` and `updated_at`)
    to any model that inherits from it. These fields automatically track
    creation and modification times.

    Fields:
        created_at (DateTimeField): Records the timestamp when an object is created.
                                    Set automatically during creation.
        updated_at (DateTimeField): Records the timestamp whenever an object is updated.
                                    Updated automatically on every save.

    Meta:
        abstract (bool): Marks this model as abstract, so it won't be created as
                         a table in the database but will be inherited by other models.
    """

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # `auto_now_add` sets the field to the current timestamp when the object is created.
    # `null=True` allows the field to be empty (useful during migrations or in certain scenarios).

    updated_at = models.DateTimeField(auto_now=True)
    # `auto_now` updates the field to the current timestamp every time the object is saved.

    class Meta:
        abstract = True
        # This model is abstract and won't be created as its own database table.


class BaseModel(TimestampModel, SoftDeleteModel):
    """
    Accumulation of multiple models which are common across project
    """

    class Meta:
        abstract = True

