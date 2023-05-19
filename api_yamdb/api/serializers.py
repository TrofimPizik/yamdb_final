import datetime as dt

from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class SingUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-+\\z]'
        )]
    )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        """Проверяет невозможность создания пользователя с ником 'me'."""
        if value == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя')
        return value


class SendTokenSerializer(serializers.Serializer):
    """Сериализатор для функции предоставления токена."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-+\\z]'
        )]
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор данных пользователя и админастратора."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'email',
            'role',
        )


class UserNotAdminSerializer(serializers.ModelSerializer):
    """Сериализатор данных пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'email',
            'role',
        )
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False,)
    genre = GenreSerializer(many=True, read_only=True,)
    rating = serializers.FloatField(default=None,)

    class Meta:
        fields = '__all__'
        model = Title


class TitleAddSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug',
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True,
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username',)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'score',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(read_only=True,)
    author = SlugRelatedField(read_only=True, slug_field='username',)

    class Meta:
        fields = '__all__'
        model = Comment
