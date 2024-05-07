from django.urls import path, include
from . import views

app_name = 'dishes'

urlpatterns = [
    path('menu/all/', views.menu, name='menu'),
    path('menu/<slug:category_slug>/<slug:dish_slug>/', views.dish, name='dish'),
    path('menu/<slug:category_slug>/', views.menu, name='category'),
]
