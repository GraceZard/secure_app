from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from audit.models import AuditLog
from .models import Item


class StockAdjustmentTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_user',
            password='StrongPass123!',
            role='admin',
        )
        self.item = Item.objects.create(
            name='Laptop',
            quantity=2,
            created_by=self.admin,
        )
        self.client.force_login(self.admin)

    def test_stock_in_updates_quantity_and_logs_action(self):
        response = self.client.post(reverse('inventory:stock_in', args=[self.item.pk]))

        self.assertRedirects(response, reverse('inventory:item_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 3)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.admin,
                action='Stock In',
                details__contains='quantity changed from 2 to 3',
            ).exists()
        )

    def test_stock_out_updates_quantity_and_logs_action(self):
        response = self.client.post(reverse('inventory:stock_out', args=[self.item.pk]))

        self.assertRedirects(response, reverse('inventory:item_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 1)
        self.assertTrue(
            AuditLog.objects.filter(
                user=self.admin,
                action='Stock Out',
                details__contains='quantity changed from 2 to 1',
            ).exists()
        )

    def test_stock_actions_reject_get_requests(self):
        response = self.client.get(reverse('inventory:stock_in', args=[self.item.pk]))

        self.assertEqual(response.status_code, 405)

    def test_stock_out_cannot_go_below_zero(self):
        self.item.quantity = 0
        self.item.save(update_fields=['quantity'])

        response = self.client.post(reverse('inventory:stock_out', args=[self.item.pk]))

        self.assertRedirects(response, reverse('inventory:item_list'))
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 0)
        self.assertFalse(AuditLog.objects.filter(action='Stock Out').exists())
