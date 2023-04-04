from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from api.permissions import OwnerOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from api.viewsets import CreateListViewSet
from posts.models import Comment, Follow, Group, Post


class PostsViewSet(ModelViewSet):
    """
    ViewSet для работы с моделью Post. Выполняет все CRUD-операции.
    Выполняет проверку, что пользователь == автор.
    Устанавливает пользователя как автором поста.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer) -> None:
        """Создание нового поста с установкой автора."""
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """
    ViewSet для работы с моделью Comment. Выполняет все CRUD-операции.
    Выполняет проверку, что пользователь == автор.
    Устанавливает пользователя как автором поста.
    """
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self) -> QuerySet[Comment]:
        """Получение списка комментариев к конкретному посту."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer: CommentSerializer) -> None:
        """Создание нового комментария с установкой автора и связи с постом."""
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ReadOnlyModelViewSet):
    """ViewSet для работы с моделью Group. Без права редактирования."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(CreateListViewSet):
    """
    ViewSet для работы с моделью Follow. Выдает список подписок
    пользователя, который отправил запрос. Создает новую подписку
    указывая пользователя в поле user.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self) -> QuerySet[Follow]:
        """Получение списка подписок пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer: FollowSerializer) -> None:
        """Создание новой подписки с установкой для поля user."""
        serializer.save(user=self.request.user)
