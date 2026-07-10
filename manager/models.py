from django.db import models
from home.models import CustomUser

class Group(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'MANAGER'})
    teacher = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'TEACHER'}, related_name='group_teacher')
    students = models.ManyToManyField(CustomUser,  limit_choices_to={'role': 'STUDENT'}, related_name='enrolled_groups')
    
    def __str__(self):
        return self.name
    

class Payment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payed_at = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'MANAGER'}, related_name='payment_receiver')
    
    def __str__(self):
        return f"{self.student.first_name} - {self.amount}"