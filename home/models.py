from django.db import models
from user.models import User

class Elective(models.Model):
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    offering_courses = models.ManyToManyField(User, related_name="offering_courses")
    seats = models.IntegerField()
    

    def __str__(self):
        return self.name