from django import forms
from .validators import validate_pdf

class CheckFileForm(forms.Form):
    pdf = forms.FileField(validators=[validate_pdf])
    email = forms.EmailField()