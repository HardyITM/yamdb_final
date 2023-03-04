from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    SlugRelatedField,
    StringRelatedField,
    ValidationError,
)
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class SignupSerializer(ModelSerializer):
    """Сериализатор для регистрации"""

    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError(
                "Вы не можете создать пользователя с таким именем"
            )
        return value


class TokenSerializer(ModelSerializer):
    """Сериализатор для получения токена"""

    confirmation_code = CharField(max_length=50, required=True)
    username = CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class UserSerializer(ModelSerializer):
    """ "Сериализатор пользователя"""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class ProfileSerializer(UserSerializer):
    """Сериализатор для пользователя "me"."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class GenreSerializer(ModelSerializer):
    """Сериализатор для жанров произведения."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(ModelSerializer):
    """Сериализатор для категории произведения."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleGetSerializer(ModelSerializer):
    """GET сериализатор для произведения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )


class TitlePostSerializer(ModelSerializer):
    """POST сериализатор для произведения."""

    category = SlugRelatedField(
        slug_field="slug",
        allow_null=False,
        queryset=Category.objects.all(),
        required=True,
    )
    genre = SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
        required=True,
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def to_representation(self, title):
        serializer = TitleGetSerializer(title)
        return serializer.data


class ReviewSerializer(ModelSerializer):
    """Сериализатор для отзыва."""

    author = StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )

    def validate(self, data):
        request = self.context.get("request")

        if request.method == "POST":
            title_id = self.context["view"].kwargs.get("title_id")
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                author=request.user, title=title
            ).exists():
                raise ValidationError("Вы уже оставили отзыв!")
        return data


class CommentSerializer(ModelSerializer):
    """Сериализатор комментариев"""

    author = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )
