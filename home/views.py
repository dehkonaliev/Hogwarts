from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, SignUpForm, UpdateMeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

@login_required
def home_page(request):
    return render(request, 'manager/mg-home.html')


def no_access(request):
    return render(request, 'utils/no-access.html')

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
            login(request, user)
            return redirect('home')
            
            
        return render(request, 'utils/signup.html', {'form': form})
    

class UpdateMeView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateMeForm(instance=request.user)
        return render(request, 'utils/update-me.html', {'form': form})

    def post(self, request):
        form = UpdateMeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
        return render(request, 'utils/update-me.html', {'form': form})
    

@login_required
def my_profile_view(request):
    context = {
        'user': request.user
    }
    
    return render(request, 'manager/my-profile.html', context)
                
        
            
            
        
        