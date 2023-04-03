import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(serializers.ImageField):
    '''
    Пользовательское поле для сериализатора Позволяет получать данные
    изображения в формате base64 и преобразовывает их в объект
    Django ContentFile.
    '''
    def to_internal_value(self, data):
        '''Преобразует данные изображения в объект ContentFile'''
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Post.'''
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post
        read_only_fields = ('id', 'pub_date', 'author')


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Comment.'''
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment
        read_only_fields = ('id', 'author', 'post', 'created')


class GroupSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Group.'''
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group
        read_only_fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Follow.'''
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        """
        Проверяет данные перед созданием новой подписки.
        Не даст подписаться на себя и создать повторную запись.
        """
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError("Нельзя подписываться на себя!")
        if Follow.objects.filter(
            user=self.context['request'].user, following=data['following']
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора!")
        return data
