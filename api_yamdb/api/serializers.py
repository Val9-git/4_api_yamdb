# import re
from django.core.validators import RegexValidator
from rest_framework import serializers

from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review  # , Comment,
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


from users.models import User
from .validators import username_validator



class UserSerializer(serializers.ModelSerializer):
    """Сериализатор обращений к users/."""
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
        max_length=254,
    )

           
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User

    def validate_username(self, value):
       return username_validator(value)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)  

    def validate_username(self, value):
        return username_validator(value)    

'''
class RegisterDataSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации и создания нового пользователя. """
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
        ],
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
        max_length=254,
    )
   
    class Meta:
        fields = ("username", "email",)
        model = User

    def validate_username(self, value):
       return username_validator(value)    
'''    
class RegisterDataSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации и создания нового пользователя. """
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
   
    class Meta:
        fields = ("username", "email",)
        model = User

    def validate_username(self, value):
       return username_validator(value)     
      

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        return username_validator(value)    


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

    rating = serializers.IntegerField(read_only=True)

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



class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для рецензий."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise ValidationError('Оценка может быть от 1 до 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Разрешён только один отзыв к произведению!')
        return data

    class Meta:
        fields = '__all__'
        model = Review

