from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin


class CreateListViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """
    Пользовательский ViewSet для POST-запроса и просмотра
    списка объектов с помощью GET-запроса.
    """
    pass
