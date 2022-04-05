"""fipe_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include
from rest_framework import routers
from . import views
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated



router = routers.DefaultRouter()
router.register('address', views.AddressViewSet)
router.register('fileUpload', views.FileViewSet)
router.register('fileUploadHistory', views.FileHistoryViewSet)

router.register(r'user', views.UserViewSet, basename='users')
router.register(r'guestUser', views.UserNonAdministratorViewSet, basename='guests')


urlpatterns = [
    path('', include(router.urls)),
]
