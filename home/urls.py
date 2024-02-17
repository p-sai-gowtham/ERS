from os import name
from django.urls import path

from . import views

name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('electives/', views.elective, name='electives'),
    path('import_customers/', views.import_students_view, name='import-students'),
    path('ad', views.ad),
]