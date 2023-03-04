from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Разрешения для Админа."""

    message = (
        "Ошибка прав доступа",
        "Действие доступно только для администратора.",
    )

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.is_staff
            or request.user.is_admin
        )


class ReadOnlyOrIsAdmin(BasePermission):
    """Разрешения Админа и авторизированного пользователя."""

    message = (
        "Ошибка прав доступа! " "Действие доступно только для администратора",
        "и авторизированного пользователя .",
    )

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class ReadOnlyOrIsAdminOrModeratorOrAuthor(BasePermission):
    """Разрешения для Модератора, автора, и админа"""

    message = (
        "Ошибка прав доступа!"
        "Действие доступно только для администратора, модератора "
        "или автора."
    )

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_moderator
                or request.user.is_admin
                or request.user == obj.author
            )
        )
