from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from inventory.models import InventoryItem, InventoryChangeLog
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class InventoryAPITestCase(APITestCase):

    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(
            username='owneruser',
            password='password123',
            role='owner'
        )

        self.worker = User.objects.create_user(
            username='workeruser',
            password='password123',
            role='worker'
        )

        # Authenticate owner using JWT
        refresh = RefreshToken.for_user(self.owner)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        # Create inventory item
        self.item = InventoryItem.objects.create(
            owner=self.owner,   
            name='Laptop',
            description='Dell Latitude',
            quantity=10,
            price=500000,
            category='Electronics'
        )

    def test_create_inventory_item(self):
        url = reverse('inventoryitem-list')
        data = {
            'name': 'Phone',
            'description': 'Samsung Galaxy',
            'quantity': 5,
            'price': 300000,
            'category': 'Electronics'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)

    def test_get_inventory_items(self):
        url = reverse('inventoryitem-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_inventory_item(self):
        url = reverse('inventoryitem-detail', args=[self.item.id])
        data = {'quantity': 15}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 15)

    def test_delete_inventory_item(self):
        url = reverse('inventoryitem-detail', args=[self.item.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InventoryItem.objects.count(), 0)

    def test_user_cannot_modify_other_users_item(self):
        # Authenticate as worker
        refresh = RefreshToken.for_user(self.worker)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

        url = reverse('inventoryitem-detail', args=[self.item.id])
        response = self.client.patch(url, {'quantity': 20}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_inventory_change_log_created(self):
        url = reverse('inventoryitem-detail', args=[self.item.id])
        self.client.patch(url, {'quantity': 20}, format='json')

        logs = InventoryChangeLog.objects.filter(item=self.item)
        self.assertTrue(logs.exists())
