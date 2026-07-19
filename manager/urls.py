from django.urls import path
from .views import (CreateGroupView, students_list, StudentProfileView, teachers_list, TeacherProfileView,
                    GroupDetailView, )

urlpatterns = [
    path('groups', CreateGroupView.as_view(), name='mg-group-list'),
    path('students', students_list, name='mg-students-list'),
    path('student-profile/<slug:username>', StudentProfileView.as_view(), name='mg-student-profile'),
    path('techers', teachers_list, name='mg-teachers-list'),
    path('teacher-profile/<slug:username>', TeacherProfileView.as_view(), name='mg-teacher-profile'),
    path('group-detail/<int:pk>', GroupDetailView.as_view(), name='mg-group-detail'),
]

