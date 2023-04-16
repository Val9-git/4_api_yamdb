# from django.conf import settings
# from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User


from reviews.models import Category, Genre, Title  # , Review

from .filters import TitlesFilter
from .permissions import IsAdmin, ReadOnly, IsAdminOrReadOnly, IsAdminModeratorOwnerOrReadOnly  # IsAuthor, IsModerator

from .serializers import (CategorySerializer, GenreSerializer, TitlePostSerializer,
                          TitleViewSerializer, ReviewSerializer, UserSerializer,
                          UserEditSerializer, TokenSerializer, RegisterDataSerializer)



@api_view(["POST"])
@permission_classes([AllowAny, ])
def register(request):
    LOGIN_ERROR = "Это имя пользователя уже занято!"
    EMAIL_ERROR = "Эта электронная почта уже занята!"
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        user, _ = User.objects.get_or_create(username=username, email=email)
    except IntegrityError:
        real_error = (
            EMAIL_ERROR
            if User.objects.filter(email=email).exists()
            else LOGIN_ERROR
        )
        return Response(real_error, status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)    


@api_view(["POST"])
@permission_classes([AllowAny, ])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет для пользователя'''
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
#    filter_backend = (SearchFilter,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ('username')

    @action(
        methods=[
            "GET",
            "PATCH"
        ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(user)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)  


'''
class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецензий."""




class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

'''

class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet
                        ):
    """Вьюсет для Категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet
                    ):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all()
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePostSerializer
        return TitleViewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецензий."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
