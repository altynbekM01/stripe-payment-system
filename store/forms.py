# store/forms.py

from django import forms

class PromoCodeForm(forms.Form):
    code = forms.CharField(label="Промокод", max_length=255)
