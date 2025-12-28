from rest_framework.routers import DefaultRouter
from .views import  InventoryItemViewSet, InventoryChangeLogViewSet, UserViewSet

router = DefaultRouter()
router.register('items', InventoryItemViewSet, basename= 'items')
router.register('logs', InventoryChangeLogViewSet, basename= 'logs')
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls

