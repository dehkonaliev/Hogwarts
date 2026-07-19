from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Group, Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GroupForm
from django.db.models import Q, F
from home.models import CustomUser
from student.models import StudentInfo
from decimal import Decimal, InvalidOperation


def is_manager(request):
    if request.user.role != 'MANAGER':
        return redirect('no-access')
    return None
    
   
class CreateGroupView(LoginRequiredMixin, View):
    def get(self, request):
        access_check = is_manager(request)
        if access_check:
            return access_check
        groups = Group.objects.all().order_by('-id')
        search_query = request.GET.get('group-name', '')
        teacher = request.GET.get('teacher')
        if search_query:
            groups = groups.filter(Q(name__icontains=search_query) & Q(teacher=teacher))
        
        form = GroupForm() 
        return render(request, 'manager/group-list.html', {'groups': groups, 'form': form})
    
    def post(self, request):
        access_check = is_manager(request)
        if access_check:
            return access_check
            
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mg-group-list')
        
        groups = Group.objects.all().order_by('-id')
        return render(request, 'manager/group-list.html', {'groups': groups, 'form': form})
    
@login_required
def students_list(request):
    access_check = is_manager(request)
    if access_check:
        return access_check
    students = CustomUser.objects.filter(role='STUDENT')
    context = {
        'students': students
    }
    
    return render(request, 'manager/students.html', context)


class StudentProfileView(View):
    def get(self, request, username):
        access_check = is_manager(request)
        if access_check:
            return access_check
        user = CustomUser.objects.filter(username=username).first()
        student_info = StudentInfo.objects.get(student=user)
        
        if not user or user.role != 'STUDENT':
            return redirect('not-found')  
                
        groups = user.enrolled_groups.all()
        
        available_groups = Group.objects.exclude(id__in=groups.values_list('id', flat=True))
        
        context = {
            'student': user,
            'groups': groups,
            'available_groups': available_groups,
            'student_info': student_info
        }
        return render(request, 'manager/mg-student-profile.html', context)
    
    def post(self, request, username):
        group = request.POST.get('group', None)
        user = CustomUser.objects.filter(username=username).first()
        
        if group:
            group = Group.objects.get(pk=group)
            if 'add' in request.POST:
                group.students.add(user)
                
            elif 'remove' in request.POST:
                group.students.remove(user)
        
        payment = request.POST.get('amount', 0)
        student_info = StudentInfo.objects.filter(student=user).first()
        
        if payment and 'payment' in request.POST:
            payment = Decimal(payment)
            student_info.balance = student_info.balance + payment
            student_info.save()
            return redirect('mg-student-profile', user.username)
            
                
            
        groups = user.enrolled_groups.all()
        
        available_groups = Group.objects.exclude(id__in=groups.values_list('id', flat=True))
        
        
        context = {
            'student': user,
            'groups': groups,
            'available_groups': available_groups,
            'student_info': student_info
        }
        return render(request, 'manager/mg-student-profile.html', context)
        
    
    
@login_required
def teachers_list(request):
    access_check = is_manager(request)
    if access_check:
        return access_check
    teachers = CustomUser.objects.filter(role='TEACHER')
    context = {
        'teachers': teachers
    }
    
    return render(request, 'manager/teachers.html', context)


class TeacherProfileView(View):
    def get(self, request, username):
        user = CustomUser.objects.filter(username=username).first()
        if not user or user.role != 'TEACHER':
            return redirect('not-found')
        
        groups = user.group_teacher.all()
        context = {
            'teacher': user,
            'groups': groups
        }
        return render(request, 'manager/mg-teacher-profile.html', context)
    
    
class GroupDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        access_check = is_manager(request)
        if access_check:
            return access_check
        
        group = get_object_or_404(Group, pk=pk)
        teachers = CustomUser.objects.filter(role='TEACHER')
        
        students = group.students.all()
        context = {
            'group': group,
            'students': students,
            'teachers': teachers
        }
        
        return render(request, 'manager/mg-group-detail.html', context)
    
    def post(self, request, pk):
        access_check = is_manager(request)
        if access_check:
            return access_check
        teachers = CustomUser.objects.filter(role='TEACHER')
        
        teacher = teachers.filter(pk=request.POST.get('teacher')).first()
        group = get_object_or_404(Group, pk=pk)
        
        if teacher:
            group.teacher = teacher
            group.save()
        
        students = group.students.all()
        context = {
            'group': group,
            'students': students,
            'teachers': teachers
        }
        
        return render(request, 'manager/mg-group-detail.html', context)
        
    
    
    
        

