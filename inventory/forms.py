from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'price', 'category', 'image']  # add price, category, image

    def clean_name(self):
        name = self.cleaned_data['name']
        import re
        # Whitelist: only letters, spaces, hyphens, and apostrophes
        if not re.match(r'^[A-Za-z\s\-\']+$', name):
            raise forms.ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes.")
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity