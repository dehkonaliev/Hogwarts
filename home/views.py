from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

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
                
        
            
            
        
        