from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models
from reviews.abstract_model import Genre_Category_Abstract
import datetime as dt


class Category(Genre_Category_Abstract):

    class Meta(Genre_Category_Abstract.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_category_slug'
            )
        ]


class Genre(Genre_Category_Abstract):

    class Meta(Genre_Category_Abstract.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_genre_slug'
            )
        ]


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.PositiveSmallIntegerField('год выпуска',
                                            db_index=True,
                                            validators=MaxValueValidator(
                                                dt.date.today().year))
    description = models.TextField('Описание',
                                   blank=True)
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 verbose_name='категория')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')

    class Meta:
        ordering = ('-name',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField('имя пользователя',
                                max_length=150,
                                unique=True,
                                validators=[
                                    RegexValidator(
                                        regex=r'^[\w.@+-]+\Z',
                                        message='Не соответствует Regex!'
                                    )
                                ])
    email = models.EmailField('email', max_length=254, unique=True)
    role = models.CharField(
        'роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    bio = models.TextField('биография', blank=True)
    confirmation_code = models.CharField('код подтверждения',
                                         max_length=4)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('-username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username


class Review(models.Model):
    text = models.TextField('текст')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='произведение')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='автор')
    score = models.PositiveSmallIntegerField(verbose_name='оценка',
                                             validators=[
                                                 MinValueValidator(1),
                                                 MaxValueValidator(10)
                                             ])
    pub_date = models.DateTimeField('дата публикации',
                                    auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    text = models.TextField('текст')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='отзыв')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор')
    pub_date = models.DateTimeField('дата публикации',
                                    auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:10]
