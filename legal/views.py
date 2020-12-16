from django.shortcuts import render


def about(request):
    return render(request, 'about.html')


def tech(request):
    return render(request, 'tech.html')
