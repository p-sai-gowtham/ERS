from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None,  **extra_fields):
        extra_fields = {"is_staff": False, "is_superuser": False, **extra_fields}
        if not email:
            raise ValueError("Users must have an email address")
        if first_name and last_name:
            user = User(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        else:
            user = User(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields = {
            "dashboard": True,
            "customer": True,
            "admin": True,
            "finance": True,
            "hr": True,
            "is_staff": True,
            "is_superuser": True,
            **extra_fields,
        }

        user = self.create_user(email=email, password=password,  **extra_fields)

        return user

USER_CHOICES = [
    ('employee', 'Employee'),
    ('HR', 'HR'),
    ('Admin', 'Admin'),
]
class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100, unique=True)
    jntu_no = models.CharField(max_length=20, unique=True)
    USERNAME_FIELD = 'email'
    department = models.CharField(max_length=20, default='employee')
    email = models.EmailField(_('email address'), unique=True)
    current_sem = models.IntegerField(default=1)
    
    objects = UserManager()

class Elective(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    elective_name = models.CharField(max_length=100)
    offering_department = models.CharField(max_length=100)
    offering_strength = models.IntegerField()
    not_allowed_students = models.ManyToManyField(User, blank=True)