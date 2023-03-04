from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    views,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    ReadOnlyOrIsAdmin,
    ReadOnlyOrIsAdminOrModeratorOrAuthor,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ProfileSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TokenSerializer,
    UserSerializer,
)


class APISignup(views.APIView):
    """Регистрация пользователя."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        user = User.objects.create(username=username, email=email)
        token = default_token_generator.make_token(user)
        send_mail(
            subject="Ваш код для api-токена.",
            message=f"Код: {token}",
            from_email="test_user@yandex.ru",
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateToken(views.APIView):
    """Выдача токена"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data["confirmation_code"]
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
        return Response(
            "Confirm code invalid", status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = "username"

    @action(
        methods=("get", "patch"),
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=ProfileSerializer,
        url_path="me",
    )
    def me(self, request, pk=None):
        user = User.objects.get(username=request.user.username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведения."""

    permission_classes = (ReadOnlyOrIsAdmin,)
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).order_by(
        "id"
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вюьсет отзывов"""

    permission_classes = (ReadOnlyOrIsAdminOrModeratorOrAuthor,)
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class ListCreateDesctroyViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    """Базовый вьюсет для получения списка, создания и удаления объекта"""

    pass


class CategoryViewSet(ListCreateDesctroyViewSet):
    """Вьюсет для категории произведения."""

    permission_classes = (ReadOnlyOrIsAdmin,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDesctroyViewSet):
    """Вьюсет для жанров произведения."""

    permission_classes = (ReadOnlyOrIsAdmin,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев"""

    permission_classes = (ReadOnlyOrIsAdminOrModeratorOrAuthor,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs["title_id"]
        review_id = self.kwargs["review_id"]
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        serializer.save(author=self.request.user, review=review)
