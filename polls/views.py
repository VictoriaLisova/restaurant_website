from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Home',
        'content': 'dsofpsp'
    }
    return render(request, "restaurant_website/index.html", context)


def about(request):
    return HttpResponse('About page')
