from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
import pandas as pd
from user.models import User

# Create your views here.
def home(request):
    return render(request, 'student/index.html')

def elective(request):
    return render(request, 'student/electives.html')

def ad(request):
    return render(request, 'ad/index.html')

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

    return render(request, "home/import_students.html", {"excel_columns": excel_columns})