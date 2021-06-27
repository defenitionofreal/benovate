from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserListView, UserDetailView, TransferCreateView, TransferViewSet, index_redirect

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'transfers', TransferViewSet)

urlpatterns = [
    path('', index_redirect),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('transfer/', TransferCreateView.as_view(), name='transfer-form'),
    path('api/v1/', include(router.urls)),
]
