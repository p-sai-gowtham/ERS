from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('electives/', views.elective, name='electives'),
    path('adminr/', views.admin, name='admin'),
]