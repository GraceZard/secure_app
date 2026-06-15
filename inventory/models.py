from django.db import models
from django.conf import settings
from auditlog.registry import auditlog

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('women', 'Women'),
        ('men', 'Men'),
        ('beauty', 'Beauty'),
        ('technology', 'Technology'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=49.90)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='women')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

auditlog.register(Item)