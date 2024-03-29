from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для Пользователей."""

    list_display = ("username", "first_name", "last_name", "email", "role")
    list_editable = ("role",)
    list_filter = ("role",)
    search_fields = ("username",)
    empty_value_display = "-пусто-"
