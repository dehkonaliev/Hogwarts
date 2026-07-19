from django.db import models
from home.models import CustomUser
from teacher.models import Homework, Lesson

class StudentSubmit(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, limit_choices_to={'role':'STUDENT'}, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    file = models.FileField(upload_to='submissions/')
    xp_earned = models.PositiveIntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.student.first_name
    
class StudentInfo(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'}, related_name='student_info')
    xp = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    
    def __str__(self):
        return self.student.first_name
    