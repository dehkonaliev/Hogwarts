from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('MANAGER', 'Manager'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone_num = models.CharField(max_length=12, blank=True, null=True)
    profile_img = models.ImageField(upload_to='avtrs/', default='default_user.jpg', blank=True)
    
