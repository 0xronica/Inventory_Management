from rest_framework import serializers
from django.contrib.auth.models import User
from .models import InventoryItem, InventoryChangeLog

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            'id',
            'name',
            'description',
            'quantity',
            'price',
            'category',
            'date_added',
            'last_updated',
        ]
        read_only_fields = ['date_added', 'last_updated']

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be zero or greater.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be zero or greater.")
        return value


class InventoryChangeLogSerializer(serializers.ModelSerializer):
    inventory_item = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = InventoryChangeLog
        fields = [
            'id',
            'inventory_item',
            'user',
            'old_quantity',
            'new_quantity',
            'time_stamp',
        ]

