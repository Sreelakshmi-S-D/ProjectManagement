from django import forms
from .models import *

class LoginDetailsForm(forms.Form):
    File = forms.FileField()
    class Meta:
        widgets={
            'File':forms.FileInput(attrs={'class':'form-control'})
        }