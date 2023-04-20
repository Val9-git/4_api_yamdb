from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    register)

router_api_v1 = DefaultRouter()


router_api_v1.register(
    'titles',
    TitleViewSet, basename='titles'
)
router_api_v1.register(
    'categories',
    CategoriesViewSet, basename='categories'
)
router_api_v1.register(
    'genres',
    GenresViewSet, basename='genres'
)


router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)


router_api_v1.register(r'users', UserViewSet, basename='users')

router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
