from rest_framework import viewsets
from django.db.models import Q
from .models import User
from .models import Address
from .models import File
from .models import FileHistory
from .models import PageNumberPagination
from .serializers import UserSerializer
from .serializers import UserNonAdminSerializer
from .serializers import AddressSerializer
from .serializers import FileSerializer
from .serializers import FileHistorySerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import logging


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):

        q = Q()

        qs = super().get_queryset()
        # filtro por nomeIsAuthenticated
        if 'nome' in self.request.GET:
            q &= Q(nome__icontains=self.request.GET['nome'])

        # filtro por funcao
        if 'email' in self.request.GET:
            q &= Q(email__icontains=self.request.GET['email'])

        if 'active' in self.request.GET:
            q &= Q(is_active__icontains=self.request.GET['ativo'])

        if 'guestUsers' in self.request.GET:
            q &= Q(is_staff=False)

        return qs.filter(q)


class UserNonAdministratorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserNonAdminSerializer

    def get_queryset(self):

        q = Q()

        qs = super().get_queryset()
        # filtro por nomeIsAuthenticated
        if 'nome' in self.request.GET:
            q &= Q(nome__icontains=self.request.GET['nome'])


        return qs.filter(q)



class AddressViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class FileViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileHistoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FileHistory.objects.all()
    serializer_class = FileHistorySerializer

    # def get_queryset(self):
    #     q = Q()
    #     qs = super().get_queryset()
    #     # if 'curso' in self.request.GET:
    #     #     q &= Q(curso=self.request.GET['curso'])
    #     return qs.filter(q)
