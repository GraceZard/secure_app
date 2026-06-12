from django.db import models
from django.conf import settings
from auditlog.registry import auditlog   # <-- ADD THIS LINE

class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Register the model to be audited
auditlog.register(Item)   # <-- ADD THIS LINE AT THE END