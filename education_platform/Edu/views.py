from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import (
    Course,
)

from .serializers import CourseSerializer


class CourseViewSet(viewsets.ViewSet):
    

    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        applications = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(applications)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
