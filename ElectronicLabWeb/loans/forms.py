# loans/forms.py
from django import forms
from inventory.models import Component
from .models import LoanCart

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = LoanCart
        fields = ['component', 'cantidad']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['component'].queryset = Component.objects.filter(stock__gt=0)