from django import forms
from inventory.models import Component, Category

class ComponentForm(forms.ModelForm):
    image_file = forms.FileField(required=False, label="Imagen del componente")
    datasheet_file = forms.FileField(required=False, label="Datasheet (PDF)")

    class Meta:
        model = Component
        fields = ['code', 'description', 'location', 'stock', 'categories']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control auto-expand',
                'rows': 2,
                'placeholder': 'Descripción del componente...'
            })
        }