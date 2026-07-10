from django.shortcuts import render


def home_page(request):
    return render(request, 'manager/mg-home.html')


def no_access(request):
    return render(request, 'utils/no-access.html')