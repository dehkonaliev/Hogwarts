from django.shortcuts import render, redirect, get_object_or_404
from home.models import CustomUser
from manager.models import Group
from teacher.models import Lesson, Homework
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import StudentSubmit, StudentInfo
from django.db.models import Exists, OuterRef, Prefetch
from .forms import HomeworkForm
from django.db.models import Q


@login_required
def group_list_view(request):
    groups = request.user.enrolled_groups.all()
    
    context = {
        'groups': groups
    }
    return render(request, 'student/st-group-list.html', context)


class GroupDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        
        user = request.user
        group = Group.objects.get(pk=pk)
        if user not in group.students.all():
            return redirect('no-access')
        
        students = group.students.all()
        lessons = Lesson.objects.filter(group=group).order_by('-id')
        context = {
            'group': group,
            'students': students,
            'lessons': lessons
        }
        return render(request, 'student/st-group-detail.html', context)


class LessonDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):        
        user = request.user
        lesson = Lesson.objects.get(pk=pk)
        if user not in lesson.group.students.all():
            return redirect('no-access')
        
        homeworks = Homework.objects.filter(lesson=lesson).order_by('-id')
        context = {
            'lesson': lesson,
            'homeworks': homeworks
        }
        return render(request, 'student/st-lesson-detail.html', context)
    
    
class HomeworkDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        homework = Homework.objects.get(pk=pk)
        submit = StudentSubmit.objects.filter(Q(homework=homework) & Q(student=user)).first()
        form = HomeworkForm(instance=submit)
        context = {
            'homework': homework,
            'form': form,
            'submission': submit,
        }
        
        return render(request, 'student/st-homework-detail.html', context)
    
    def post(self, request, pk):
        user = request.user
        homework = Homework.objects.get(pk=pk)
        submit = StudentSubmit.objects.filter(Q(homework=homework) & Q(student=user)).first()
        if submit:
            form = HomeworkForm(request.POST, request.FILES, instance=submit)
        else:
            form = HomeworkForm(request.POST, request.FILES)
            
        if form.is_valid():
            home = form.save(commit=False)
            home.homework = homework
            home.student = user
            home.save()
            
        context = {
            'homework': homework,
            'form': form,
            'submission': submit,
        }
        
        return render(request, 'student/st-homework-detail.html', context)
        