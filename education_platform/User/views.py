from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    StudentApplicationSerializer,
    GroupSerializer,
)
from .models import (
    Student_application,
    User,
    Group,
)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class StudentApplicationViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Student_application.objects.all()
        serializer = StudentApplicationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Student_application.objects.all()
        applications = get_object_or_404(queryset, pk=pk)
        serializer = StudentApplicationSerializer(applications)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # this method make application approved
        instance = Student_application.objects.get(pk=pk)
        instance.is_approved = True
        instance.save()
        serializer = StudentApplicationSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = StudentApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        applications = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(applications)
        return Response(serializer.data)


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Group.objects.all()
        applications = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(applications)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = StudentApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



