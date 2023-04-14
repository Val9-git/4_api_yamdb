# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from reviews.models import Category, Genre, Title

from .filters import TitlesFilter
from .permissions import IsAdmin, ReadOnly  # IsAuthor, IsModerator
from .serializers import (CategorySerializer, GenreSerializer, TitlePostSerializer,
                          TitleViewSerializer, RegistrationSerializer, LoginSerializer,)
                      
from .renderers import UserJSONRenderer

User = get_user_model()

'''
class SignUpAPIView(CreateAPIView):
    """Создать пользователя и отправить код на почту."""



class TokenObtainView(TokenObtainPairView):
    """Получить токен доступа по коду из письма."""

'''

class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        # Cоздание сериализатора, валидация и сохранение 
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class LoginAPIView(APIView):
    """
    Разрешить аутентифицированному пользователю войти в учетную запись.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)    
   
    
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

'''
class UsersAPIView(ListCreateAPIView):
    """
    Администратор получает список зарегистрированных
    пользователей и может добавить нового.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = LimitOffsetPagination
    search_fields = ('=username',)


class ProfileAPIView(RetrieveUpdateDestroyAPIView):
    """Профили пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'


class SelfProfileAPIView(RetrieveUpdateAPIView):
    """Профиль пользователя, который он может редактировать."""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def partial_update(self, request):
        request_role = self.request.user.role
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request_role == 'user':
            serializer.validated_data['role'] = 'user'
            serializer.save()
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''