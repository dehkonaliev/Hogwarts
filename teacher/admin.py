from django.contrib import admin
from .models import Attendance, Lesson, Homework

admin.site.register(Attendance)
admin.site.register(Lesson)
admin.site.register(Homework)