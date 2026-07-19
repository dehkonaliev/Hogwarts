from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, SignUpForm, UpdateMeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from manager.models import Group
from student.models import StudentInfo

@login_required
def home_page(request):
    user = request.user
    if user.role == 'MANAGER':
        groups_count = Group.objects.count()
        teachers_count = CustomUser.objects.filter(role='TEACHER').count()
        students_count = CustomUser.objects.filter(role='STUDENT').count()
        managers_count = CustomUser.objects.filter(role='MANAGER').count()
        
        context = {
            'groups_count':groups_count,
            'teachers_count':teachers_count,
            'students_count':students_count,
            'managers_count':managers_count
        }
        
        return render(request, 'manager/mg-home.html', context)
    
    elif user.role == 'TEACHER':
        groups_count = Group.objects.count()
        teachers_count = CustomUser.objects.filter(role='TEACHER').count()
        
        context = {
            'groups_count':groups_count,
        }
        
        return render(request, 'teacher/tr-home.html', context)
    


def no_access(request):
    return render(request, 'utils/no-access.html')

def not_found(request):
    return render(request, 'utils/not-found.html')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'utils/login.html', {'form': form})
    
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                raise ValidationError("Username or password is incorrect!")
            
        return render(request, 'utils/login.html', {'form': form})
    
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'utils/signup.html', {'form': form})
    
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            StudentInfo.objects.create(student=user)
            login(request, user)
            return redirect('home')
            
            
        return render(request, 'utils/signup.html', {'form': form})
    

class UpdateMeView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateMeForm(instance=request.user)
        if request.user.role == 'TEACHER':
            template_name = 'tr-base.html'
        elif request.user.role == 'MANAGER':
            template_name = 'tr-base.html'
        else:
            template_name = 'st-base.html'
        return render(request, 'utils/update-me.html', {'form': form, 'template_name': template_name})

    def post(self, request):
        form = UpdateMeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
        if request.user.role == 'TEACHER':
            template_name = 'tr-base.html'
        elif request.user.role == 'MANAGER':
            template_name = 'tr-base.html'
        else:
            template_name = 'st-base.html'
        return render(request, 'utils/update-me.html', {'form': form, 'template_name': template_name})
    

@login_required
def my_profile_view(request):
    if request.user.role == 'TEACHER':
        template_name = 'tr-base.html'
    elif request.user.role == 'MANAGER':
        template_name = 'mg-base.html'
    else:
        template_name = 'st-base.html'
    context = {
        'user': request.user,
        'template_name': template_name
    }
    
    return render(request, 'utils/my-profile.html', context)

@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')
                
        
            
            
        
        