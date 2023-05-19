from rest_framework import permissions
from users.models import User


class IsUserOrEmployee(permissions.BasePermission):
    def has_object_permission(self, req, view, user: User) -> bool:
        return req.user.is_employee or user.email == req.user.email
