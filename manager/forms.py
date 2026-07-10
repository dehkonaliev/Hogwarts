from django import forms
from .models import Group, Payment

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'teacher']