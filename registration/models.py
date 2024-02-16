from django.db import models
from user.models import User
from home.models import Elective
# Create your models here.
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Elective, on_delete=models.CASCADE)
    