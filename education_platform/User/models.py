from django.db import models
from django.contrib.auth.models import AbstractUser
from Edu.models import Course
import uuid

# Create your models here.
class User(AbstractUser):
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    user_types = [
        ('Student', "Student"),
        ('Courator', "Courator"),
        ('Teacher', "Teacher"),
        ('Comission', "Comission"),
        ('Admin', "Admin")
    ]
    user_type = models.CharField(choices=user_types, max_length=50, blank=True, null=True)


class Student_application(models.Model):
    student = models.ForeignKey("User.User", on_delete=models.CASCADE)
    boss_first_name = models.CharField(max_length=20, blank=True, null=True)
    boss_second_name = models.CharField(max_length=20, blank=True, null=True)
    boss_patronymic = models.CharField(max_length=20, blank=True, null=True)
    department_name = models.CharField(max_length=50, blank=True, null=True)
    working_position = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(max_length=300, blank=True, null=True)
    achievements = models.TextField(max_length=500, blank=True, null=True)
    motivational_letter = models.TextField(max_length=800, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)


class Group(models.Model):
    course = models.ForeignKey("Edu.Course", on_delete=models.CASCADE)
    courator = models.ForeignKey("User.User", on_delete=models.PROTECT, limit_choices_to={'user_type': 'Courator'})


class Students_Groups(models.Model):
    student = models.ForeignKey("User.User", on_delete=models.PROTECT, limit_choices_to={'user_type': 'Student'})
    group = models.ForeignKey("User.Group", on_delete=models.CASCADE)

