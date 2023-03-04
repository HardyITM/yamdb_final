from dataclasses import dataclass

from django.contrib.auth.models import AbstractUser
from django.db import models


@dataclass
class UserRole:
    """Класс для ролей пользователя."""

    DEFAULT_USER: str = "user"
    MODERATOR: str = "moderator"
    ADMIN: str = "admin"


ROLE_CHOICES = (
    (UserRole.DEFAULT_USER, "Пользователь"),
    (UserRole.MODERATOR, "Модератор"),
    (UserRole.ADMIN, "Админ"),
)


class User(AbstractUser):
    """Описание модели Юзера."""

    username = models.CharField(
        "Логин",
        max_length=150,
        unique=True,
        help_text="Ник пользователя",
    )
    email = models.EmailField(
        "e-mail",
        max_length=254,
        unique=True,
        help_text="Электронная почта",
    )
    bio = models.TextField(
        "Биография",
        blank=True,
        help_text="Биография пользователя",
    )
    role = models.TextField(
        "Роль",
        choices=ROLE_CHOICES,
        default=UserRole.DEFAULT_USER,
        help_text="Роль пользователя",
    )

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN or self.is_staff or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta:
        """Мета класс для модели."""

        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        """Возвращает удобное для человека представление."""
        return self.username
