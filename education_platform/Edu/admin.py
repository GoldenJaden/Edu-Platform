from django.contrib import admin
from .models import Lesson, Homework_submission, Atachments, Course

# Register your models here.

admin.site.register(Lesson)
admin.site.register(Homework_submission)
admin.site.register(Atachments)
admin.site.register(Course)