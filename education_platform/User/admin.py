from django.contrib import admin
from .models import User, Student_application, Group, Students_Groups, Course

# Register your models here.
admin.site.register(User)
admin.site.register(Student_application)
admin.site.register(Group)
admin.site.register(Students_Groups)
