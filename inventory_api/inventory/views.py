from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .models import InventoryItem, InventoryChangeLog
from .serializers import UserSerializer,  InventoryItemSerializer, InventoryChangeLogSerializer
from .permissions import IsOwnerOrWorker 
from django.contrib.auth import get_user_model


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrWorker]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['name', 'quantity', 'price', 'date_added']


    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        item = self.get_object()
        old_quantity = item.quantity
        updated_item = serializer.save()

        if old_quantity != updated_item.quantity:
            InventoryChangeLog.objects.create(
                item=updated_item,
                changed_by=self.request.user,
                old_quantity=old_quantity,
                new_quantity=updated_item.quantity
            )


class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryChangeLog.objects.filter(
            item__owner=self.request.user
        )
