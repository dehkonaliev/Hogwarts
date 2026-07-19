from django import forms
from .models import Lesson, Homework

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'