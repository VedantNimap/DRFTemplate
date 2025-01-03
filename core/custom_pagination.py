from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for paginating API responses using the
    PageNumberPagination style from Django REST Framework (DRF).

    Attributes:
        page_size (int): The default number of items to display per page.
                         Defaults to 10.
        page_query_param (str): The query parameter name for the page number.
                                Defaults to "page".
        page_size_query_param (str): The query parameter name to allow clients
                                     to set a custom page size. Defaults to "size".
    """

    page_size = 10  # Sets the default number of items per page.
    page_query_param = (
        "page"  # Specifies the query parameter for accessing specific pages.
    )
    page_size_query_param = (
        "size"  # Allows clients to override the default page size via query.
    )