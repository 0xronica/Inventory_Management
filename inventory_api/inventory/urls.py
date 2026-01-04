from rest_framework.routers import DefaultRouter
from .views import  InventoryItemViewSet, InventoryChangeLogViewSet, UserViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='inventoryitem')
router.register(r"inventory", InventoryItemViewSet, basename="inventory")
router.register(r'logs', InventoryChangeLogViewSet, basename= 'logs')
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls

