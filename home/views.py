from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
import pandas as pd
from user.models import User
from .models import Elective
from django.db import models
from collections import defaultdict

# Create your views here.
def home(request):
    return render(request, 'student/index.html')

def elective(request):
    return render(request, 'student/electives.html')

def ad(request):
    return render(request, 'ad/index.html')

def elect(request):
    return render(request, 'ad/elect.html')

def import_students_view(request):
    excel_columns = []
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        df = pd.read_excel(excel_file)
        excel_columns = df.columns.tolist()
        column_mappings = []
        for i, column in enumerate(excel_columns):
            # Retrieve user's selection for each column
            attribute = request.POST.get(f"column{i}", "")
            column_mappings.append(attribute)
        print(column_mappings)

            

        for index, row in df.iterrows():
            student_data = {}
            for i, column in enumerate(excel_columns):
                student_data[column_mappings[i]] = row[i]
            print(student_data)
            student = User.objects.create(**student_data)
        messages.success(request, "Customers imported successfully.")
        return redirect("app:import_customers")


def import_electives_view(request):
    excel_columns = []
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        df = pd.read_excel(excel_file)
        excel_columns = df.columns.tolist()
        column_mappings = []
        for i, column in enumerate(excel_columns):
            # Retrieve user's selection for each column
            attribute = request.POST.get(f"column{i}", "")
            column_mappings.append(attribute)

        for index, row in df.iterrows():
            student_data = {}
            for i, column in enumerate(excel_columns):
                student_data[column_mappings[i]] = row[i]
            print(student_data)
            student = Elective.objects.create(**student_data)
        messages.success(request, "Customers imported successfully.")
        return redirect("app:import_customers")

import csv
from django.http import HttpResponse

def allocate_electives(request):
    if request.method == 'POST':
        student_jntu_no = request.POST.get('student_jntu_no')
        elective_course_code = request.POST.get('elective_course_code')

        student = User.objects.get(jntu_no=student_jntu_no)
        elective = Elective.objects.get(course_code=elective_course_code)

        # Check if the student is from the offering department
        if student.dept == elective.dept:
            csv_data = [
            ['Student Name', 'JNTU Number', 'Department', 'Elective Name', 'Offering Department'],
            [student.username, student.jntu_no, student.dept, None,None]
        ]

        # Calculate proportional offering strength for each department
        total_students = User.objects.count()
        total_electives = defaultdict(int)
        for i in Elective.objects.all():
            total_electives[i.dept] += i.strength
        department_offering_strength = {}
        for k,v in total_electives.items():
            proportional_strength = int((v / total_students) * elective.strength)
            department_offering_strength[k] = proportional_strength


            # Check if the elective is already at capacity
            if elective.strength <= elective.seats.count():
                csv_data = [
                ['Student Name', 'JNTU Number', 'Department', 'Elective Name', 'Offering Department'],
                [student.username, student.jntu_no, student.dept, None, None]
            ]

            # Check if the student has already selected an elective
            if student in elective.seats.all():
                pass

            # Check if the student's department has reached its proportional strength
            if elective.dept in department_offering_strength:
                if elective.seats.filter(department=student.dept).count() >= department_offering_strength[student.dept]:
                    while proportional_strength[student.dept] <= elective.seats.filter(department=student.dept).count():
                        csv_data = [
                ['Student Name', 'JNTU Number', 'Department', 'Elective Name', 'Offering Department'],
                [student.username, student.jntu_no, student.dept, elective.name, elective.dept]
            ]


            # Add the student to the elective and update the CSV data
            elective.seats.add(student)

            # Save allocated data to CSV
            csv_data = [
                ['Student Name', 'JNTU Number', 'Department', 'Elective Name', 'Offering Department'],
                [student.username, student.jntu_no, student.dept, elective.name, elective.dept]
            ]

            filename = 'allocated_students.csv'
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            writer = csv.writer(response)
            writer.writerows(csv_data)

            allocated_file_url = response.request.build_absolute_uri()
        
        students = User.objects.all()
        electives = Elective.objects.all()
    # Return the rendered template with the file URL
        return render(request, 'student/electives.html', {'allocated_file_url': allocated_file_url, 'students': students, 'electives': electives})

