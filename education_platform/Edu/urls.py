from .views import (
    CourseViewSet,
)
from django.urls import path

app_name = "Edu"

urlpatterns = [
    #course api paths
    path('courses/', CourseViewSet.as_view({'get': 'list',
                                            'post': 'create'})),
    path('courses/<int:pk>', CourseViewSet.as_view({'get': 'retrieve'})),
]

