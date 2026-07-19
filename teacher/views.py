from django.shortcuts import render, redirect, get_object_or_404
from home.models import CustomUser
from manager.models import Group
from .models import Attendance, Lesson, Homework
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def is_teacher(request):
    if request.user.role != 'TEACHER':
        return redirect('no-access')
    return None

@login_required
def group_list_view(request):
    access_check = is_teacher(request)
    if access_check:
        return access_check
    
    user = request.user
    groups = Group.objects.filter(teacher=user)
    
    context = {
        'groups': groups
    }
    return render(request, 'teacher/tr-group-list.html', context)

class GroupDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        
        user = request.user
        group = Group.objects.get(pk=pk)
        if group.teacher != user:
            return redirect('no-access')
        
        students = group.students.all()
        context = {
            'group': group,
            'students': students
        }
        return render(request, 'teacher/tr-group-detail.html', context)
    
    def post(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        
        user = request.user
        group = Group.objects.get(pk=pk)
        if group.teacher != user:
            return redirect('no-access')
        
        if 'lesson' in request.POST:
            title = request.POST.get('title')
            Lesson.objects.create(title=title, group=group)
            return redirect('tr-group-detail', pk=pk)
            
        
            
        
                
                