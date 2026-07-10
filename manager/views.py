from django.shortcuts import render, redirect
from django.views import View
from .models import Group, Payment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GroupForm
from django.db.models import Q


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
    
    
        

