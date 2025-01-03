import django_filters


class ListFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    Custom filter class that combines `BaseInFilter` and `CharFilter`.

    This filter allows filtering by a list of values and also supports filtering by a single string value.
    """

    pass