from django import forms
from .models import StudentSubmit

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = StudentSubmit
        fields = ['message', 'file']