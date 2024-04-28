from django.urls import path, include, re_path
from . import views

app_name = 'dishes'

urlpatterns = [
    path('menu/all/', views.menu, name='menu'),
    # re_path(r'^menu/<slug:category_slug>/price_min={\w}&price_max={\w}&order_by={\w}', views.dish, name='dish'),
    path('menu/<slug:category_slug>/<slug:dish_slug>/', views.dish, name='dish'),
    path('menu/<slug:category_slug>/', views.menu, name='category'),
]
