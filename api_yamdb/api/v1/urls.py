from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    APISignup,
    CategoryViewSet,
    CommentViewSet,
    CreateToken,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

app_name = "api"
router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="category")
router.register("genres", GenreViewSet, basename="genre")
router.register("titles", TitleViewSet, basename="title")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", CreateToken.as_view(), name="create_token"),
    path("auth/signup/", APISignup.as_view(), name="signup"),
]
