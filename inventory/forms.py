from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']

    def clean_name(self):
        name = self.cleaned_data['name']
        import re
        # Whitelist: only letters, spaces, hyphens, and apostrophes
        if not re.match(r'^[A-Za-z\s\-\']+$', name):
            raise forms.ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes.")
        return name