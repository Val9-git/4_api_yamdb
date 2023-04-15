from django.urls import include, path  # re_path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, GenresViewSet, TitleViewSet,
                    ReviewViewSet
                    )


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


urlpatterns = [
    path('v1/', include(router_api_v1.urls)),

]
