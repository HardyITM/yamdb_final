from django.contrib import admin
from reviews.models import Category, Genre, GenreTitle, Review, Title


class GenreInline(admin.TabularInline):
    """Класс связи моделей жанра и произведения."""

    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для Произведения"""

    filter_horizontal = ("genre",)
    inlines = (GenreInline,)

    list_display = ("pk", "name", "year", "description", "category")
    search_fields = ("name", "year")
    list_filter = ("name", "year", "description", "category")
    empty_value_display = "-пусто-"
    list_editable = ("name", "year", "description", "category")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для Категорий"""

    list_display = ("pk", "name", "slug")
    search_fields = ("name", "slug")
    empty_value_display = "-пусто-"
    list_editable = ("name", "slug")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанра"""

    list_display = ("pk", "name", "slug")
    search_fields = ("name", "slug")
    empty_value_display = "-пусто-"
    list_editable = ("name", "slug")


admin.site.register(Review)
