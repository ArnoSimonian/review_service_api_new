from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import (CommentViewSet,
                       CategoryViewSet,
                       GenreViewSet,
                       ReviewViewSet,
                       MyTokenObtainApiView,
                       TitleViewSet,
                       UserRegistrationViewSet)


app_name = 'api'

v1_router = SimpleRouter()
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(r'auth/signup', UserRegistrationViewSet, basename='signup')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/',
         MyTokenObtainApiView.as_view(),
         name='token_obtain_pair')
]
