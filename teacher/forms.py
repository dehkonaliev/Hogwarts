from django import forms
from .models import Lesson, Homework

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'file', 'image']