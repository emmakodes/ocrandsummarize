from django import forms
from .models import Ocr


class ImageUpload(forms.ModelForm):
    class Meta:
        model = Ocr
        fields = ['image']