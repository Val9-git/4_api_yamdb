from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True, max_length=50, db_index=True
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'category: {self.name}, slug: {self.slug}'


class Genre(models.Model):
    """Модель жанра произведения."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(max_length=256, db_index=True)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(date.today().year)]
    )
    category = models.ForeignKey(
        Category, null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    description = models.CharField(
        max_length=250,
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles'
    )

    class Meta:
        ordering = ('category',)
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


class Review(models.Model):
    """Модель рецензии на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Укажите произведение'
    )
    text = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Ввод текста',
        help_text='Текст рецензии'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Выбор автора'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        help_text='Оценка от 1 до 10',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария к рецензии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Рецензия',
        help_text='Выбор рецензии'
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Ввод текста',
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        help_text='Ввод автора'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
