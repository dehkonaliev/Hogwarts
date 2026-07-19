from django import forms
from .models import Lesson, Homework
from student.models import StudentSubmit
from django.core.exceptions import ValidationError

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['title', 'file', 'image']
        
        

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentSubmit
        fields = ['xp_earned', 'feedback']

    def clean_xp_earned(self):
        xp = self.cleaned_data.get('xp_earned')
        
        if xp is not None and xp > 20:
            raise ValidationError("XP earned cannot exceed 20.")
        
        return xp