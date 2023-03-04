from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""

    name = models.TextField(
        "Название категории", max_length=256, db_index=True
    )
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.TextField("Название жанра", max_length=256, db_index=True)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.TextField("Название произведения")
    year = models.IntegerField("Год выпуска")
    description = models.TextField("Описание", null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="titles", null=True
    )
    genre = models.ManyToManyField(
        to=Genre, through="GenreTitle", related_name="titles"
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва"""

    text = models.TextField("Отзыв произведения")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        "Оценка", validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField("Дата публикации", default=timezone.now)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            )
        ]
        ordering = ["id"]

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["genre", "title"], name="unique_genre_title"
            )
        ]
        verbose_name = "Соответствие жанра и произведения"
        verbose_name_plural = "Таблица соответствия жанров и произведений"

    def __str__(self):
        return f"{self.genre} {self.title}"


class Comment(models.Model):
    """Модель комментариев."""

    text = models.TextField("Комментарий")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", default=timezone.now)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["id"]
