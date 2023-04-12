from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True, max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'category: {self.name}, slug: {self.slug}'


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(date.today().year)]
    )
    description = models.CharField(
        max_length=250,
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category, null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class TitleGenre(models.Model):
    """Модель для связи между произведениями и жанрами."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

'''
class Review(models.Model):
    """Модель рецензии на произведение."""
    


class Comment(models.Model):
    """Модель комментария к рецензии."""
'''
