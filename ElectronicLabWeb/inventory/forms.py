from django import forms
from inventory.models import Component, Category

class ComponentForm(forms.ModelForm):
    image_file = forms.FileField(required=False, label="Imagen del componente")
    datasheet_file = forms.FileField(required=False, label="Datasheet (PDF)")

    class Meta:
        model = Component
        fields = ['code', 'description', 'location', 'stock']