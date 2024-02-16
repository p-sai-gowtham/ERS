from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request, 'student/index.html')

def elective(request):
    return render(request, 'student/electives.html')

def admin(request):
    return render(request, 'admin/index.html')