from django.urls import path
from .views import (group_list_view, GroupDetailView, LessonDetailView,
                    HomeworkDetailView)

urlpatterns = [
    path('my-groups', group_list_view, name='st-group-list'),
    path('group-detail/<int:pk>', GroupDetailView.as_view(), name='st-group-detail'),
    path('lesson-detail/<int:pk>', LessonDetailView.as_view(), name='st-lesson-detail'),
    path('homework-detail/<int:pk>', HomeworkDetailView.as_view(), name='st-homework-detail'),
]