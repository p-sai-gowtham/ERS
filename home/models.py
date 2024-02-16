from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
class Student(models.Model):
    name = models.CharField(max_length=100)
    jntu_no = models.CharField(max_length=20, unique=True , primary_key=True)
    department = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    email = models.EmailField()
    current_semester = models.IntegerField()

    def __str__(self):
        return self.name
class Elective(models.Model):
    course_code = models.CharField(max_length=20, unique=True, )
    elective_name = models.CharField(max_length=100)
    offering_department = models.CharField(max_length=100)
    offering_strength = models.IntegerField()
    not_allowed_students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.elective_name
