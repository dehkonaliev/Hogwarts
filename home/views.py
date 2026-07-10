from django.shortcuts import render

# Create your views here.
def no_access(request):
    return render(request, 'utils/no-access.html')