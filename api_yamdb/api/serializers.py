from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category,  Genre,  Title  #  Review, Comment,
from users.models import User


User = get_user_model()

'''

class TokenObtainSerializer(serializers.Serializer):
    """Сериализатор токена доступа."""

'''

class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации и создания нового пользователя. """

    # Пароль содержит не менее 8 символов, не более 128,
    # не может быть прочитан клиентом
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # Клиент не может отправлять токен вместе с
    # запросом на регистрацию. Делаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # Поля, которые могут быть включены в запрос или ответ.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Метод create_user для создания нового пользователя.
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    '''Сериализатор входа пользователя в свою учетную запись'''
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # Убеждаемся, что пользователь ввел адрес эл. почты и пароль,
        # введенные данные соответствуют одному из пользователей
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Для входа требуется адрес электронной почты.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Для входа требуется пароль.'
            )
        # Проверяем, что предоставленные почта и пароль
        # соответствуют какому-то пользователю в базе данных.
        # Передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Пользователь с таким email и паролем не найден.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Пользователь деактивирован.'
            )
        
        # Возвращаем проверенные данные пользователя, они далее 
        # передются в методы create и update.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для рецензий."""
 



class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанра."""
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления/обновления произведений."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

'''
class UserSerializer(serializers.ModelSerializer):
    """Сериализатор обращений к users/."""

'''