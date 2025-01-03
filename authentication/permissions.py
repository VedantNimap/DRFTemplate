from rest_framework import permissions


class GroupPermission(permissions.BasePermission):
    """
    Custom permission class to dynamically determine required permissions based on HTTP method and model.

    This class leverages Django's built-in permission system to enforce access control.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has the required permission for the given request.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (View): The view being accessed.

        Returns:
            bool: True if the user has the required permission, False otherwise.
        """
        app_model = getattr(view, "app_model", None)
        required_permission = find_permission(app_model, request)
        # print(request.user.get_all_permissions())
        # print("Required Perms",required_permission)

        # Check if the user has the required permission
        return request.user.has_perm(required_permission)


def find_permission(app_model, request):
    """
    Determines the required permission based on the HTTP method and model.

    Args:
        app_model (tuple): A tuple containing the app name and model name.
        request (HttpRequest): The incoming HTTP request.

    Returns:
        str: The required permission string.
    """

    if request.method == "GET":
        return f"{app_model[0]}.view_{app_model[1]}"
    elif request.method == "POST":
        return f"{app_model[0]}.add_{app_model[1]}"
    elif request.method == "PUT":
        return f"{app_model[0]}.change_{app_model[1]}"
    elif request.method == "PATCH":
        return f"{app_model[0]}.change_{app_model[1]}"
    elif request.method == "DELETE":
        return f"{app_model[0]}.delete_{app_model[1]}"
