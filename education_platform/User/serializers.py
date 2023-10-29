from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import (
    User,
    Student_application,
    Students_Groups,
    Group,
)
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type='Student'
        )
        return user


class StudentsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students_Groups
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    course_name = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = Group
        fields = "__all__"

    def get_students(self, obj):
        # return students in this group
        selected = Students_Groups.objects.filter(
            group__id=obj.id
        ).values_list('student', flat=True)
        return selected


class UserSerializer(serializers.ModelSerializer):
    student_group = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'user_type', 'student_group']

    def get_student_group(self, obj):
        # return study group
        selected_options = Students_Groups.objects.filter(
            student__id=obj.id
        ).values_list('id', flat=True)
        return selected_options[0] if selected_options else None


class StudentApplicationSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='course.name')  # return course name by it's id

    class Meta:
        model = Student_application
        fields = "__all__"

