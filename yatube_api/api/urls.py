from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostsViewSet

router_v1 = DefaultRouter()
router_v1.register('v1/posts', PostsViewSet)
router_v1.register('v1/groups', GroupViewSet)
router_v1.register('v1/follow', FollowViewSet)
router_v1.register(
    'v1/posts/(?P<post_id>\\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]
