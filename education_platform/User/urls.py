from django.contrib import admin
from django.urls import path
from .views import (
    RegisterApi,
    StudentApplicationViewSet,
    UserViewSet,
    GroupViewSet,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "User"

urlpatterns = [
    # login and register api
    path('register/', RegisterApi.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # student application api paths
    path('applications/', StudentApplicationViewSet.as_view({'get': 'list',
                                                             'post': 'create'})),
    path('applications/<int:pk>', StudentApplicationViewSet.as_view({'get': 'retrieve',
                                                                     'put': 'update'})),

    # user api
    path('', UserViewSet.as_view({'get': 'list'})),
    path('<int:pk>', UserViewSet.as_view({'get': 'retrieve'})),

    # group api
    path('groups/', GroupViewSet.as_view({'get': 'list'})),
    path('groups/<int:pk>', GroupViewSet.as_view({'get': 'retrieve'})),
]

