from django.urls import path
from .views import CreateGroupView, students_list, StudentProfileView

urlpatterns = [
    path('groups', CreateGroupView.as_view(), name='mg-group-list'),
    path('students', students_list, name='mg-students-list'),
    path('student-profile/<slug:username>', StudentProfileView.as_view(), name='mg-student-profile')
]

