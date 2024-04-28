from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "restaurant_website/index.html", {})


def about(request):
    return render(request, "restaurant_website/about.html", {})


def contacts(request):
    return render(request, "restaurant_website/contacts.html", {})


