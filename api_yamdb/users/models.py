from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    role = models.CharField(
        choices=ROLES,
        default=USER,
        verbose_name='Уровень пользователя',
        max_length=255
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-+\\z]'
        )]
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150,
        blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150,
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name='E-Mail', max_length=254,
        unique=True
    )
    bio = models.TextField(verbose_name="О себе", blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
