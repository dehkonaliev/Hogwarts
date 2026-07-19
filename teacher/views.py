from django.shortcuts import render, redirect, get_object_or_404
from home.models import CustomUser
from manager.models import Group
from .models import Attendance, Lesson, Homework
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import HomeworkForm, SubmissionForm
from student.models import StudentSubmit, StudentInfo
from django.db.models import Exists, OuterRef, Prefetch


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
        lessons = Lesson.objects.filter(group=group)
        context = {
            'group': group,
            'students': students,
            'lessons': lessons
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
        

class LessonDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        
        user = request.user
        lesson = Lesson.objects.get(pk=pk)
        if lesson.group.teacher != user:
            return redirect('no-access')
        
        homeworks = Homework.objects.filter(lesson=lesson)
        form = HomeworkForm()
        context = {
            'lesson': lesson,
            'homeworks': homeworks,
            'form': form
        }
        return render(request, 'teacher/tr-lesson-detail.html', context)
    
    def post(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        lesson = Lesson.objects.get(pk=pk)
        if 'add-homework' in request.POST:
            form = HomeworkForm(request.POST, request.FILES)
            
            if form.is_valid():
                homework = form.save(commit=False)
                homework.lesson = lesson
                homework.save()
                
                return redirect('tr-lesson-detail', pk=pk)
            
        elif 'delete-lesson' in request.POST:
            group_id = lesson.group.pk
            lesson.delete()
            return redirect('tr-group-detail', pk=group_id)
        
        
class HomeworkDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        
        user = request.user
        homework = Homework.objects.get(pk=pk)
        submissions = StudentSubmit.objects.filter(homework=homework)
        students = homework.lesson.group.students.all().prefetch_related(
            Prefetch(
                'studentsubmit_set',
                queryset=submissions,
                to_attr='homework_submission'
            )
        )
        
        context = {
            'homework': homework,
            'students': students
        }
        
        return render(request, 'teacher/tr-homework-detail.html', context)
    
    def post(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        homework = Homework.objects.get(pk=pk)
        
        if 'delete-homework' in request.POST:
            lesson_id = homework.lesson.pk
            homework.delete()
            return redirect('tr-lesson-detail', pk=lesson_id)
        
        
class SubmissionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        submission = StudentSubmit.objects.filter(pk=pk).first()
        submission_form = SubmissionForm(instance=submission)
        context = {
            'submission': submission,
            'submission_form': submission_form
        }
        return render(request, 'teacher/tr-submission.html', context)
    
    def post(self, request, pk):
        access_check = is_teacher(request)
        if access_check:
            return access_check
        submission = StudentSubmit.objects.filter(pk=pk).first()
        submission_form = SubmissionForm(request.POST, instance=submission)
        if submission_form.is_valid():
            submit = submission_form.save(commit=False)
            xp_earned = submission_form.cleaned_data.get('xp_earned')
            submit.feedback = submission_form.cleaned_data.get('feedback')
            submit.xp_earned = xp_earned
            submit.save()
            student_info = StudentInfo.objects.filter(student=submission.student).first()
            student_info.xp = student_info.xp + xp_earned
            student_info.coins = student_info.coins + xp_earned * 5
            student_info.save()
            
        
        context = {
            'submission': submission,
            'submission_form': submission_form
        }
        return render(request, 'teacher/tr-submission.html', context)
        