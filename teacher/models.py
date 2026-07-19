from django.db import models
from home.models import CustomUser
from manager.models import Group

class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    
class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    is_present = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['lesson', 'student']
        
class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='homework_materials/', blank=True, null=True)
    image = models.ImageField(upload_to='homework_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
