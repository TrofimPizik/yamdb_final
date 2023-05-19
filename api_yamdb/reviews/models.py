from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название категории',)
    slug = models.SlugField(unique=True,)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название жанра',)
    slug = models.SlugField(unique=True,)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название произведения',
    )
    year = models.IntegerField(verbose_name='Год создания произведения',)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанр произведения',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок отзыва',
    )
    text = models.TextField(verbose_name='Текст отзыва',)
    score = models.IntegerField(
        validators=[MaxValueValidator(10)], verbose_name='Оценка',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True,)

    class Meta:
        unique_together = ('author', 'title',)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение к которому относится жанр',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genres',
        blank=True,
        null=True,
        verbose_name='Жанр',
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв',
    )
    text = models.TextField(verbose_name='Текст комментария',)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True,
    )
