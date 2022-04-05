from rest_framework import viewsets
from django.db.models import Q
from .models import User
from .models import Address
from .models import File
from .models import FileHistory
from .models import PageNumberPagination
from .serializers import UserSerializer
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

        # filtro por código
        if 'codigo' in self.request.GET:
            q &= Q(id=int(self.request.GET['codigo']))

        if 'código' in self.request.GET:
            q &= Q(id=int(self.request.GET['código']))
        # filtro por nomeIsAuthenticated
        if 'nome' in self.request.GET:
            q &= Q(nome__icontains=self.request.GET['nome'])

        # filtro por funcao
        if 'status' in self.request.GET:
            if self.request.GET['status'].lower() in "sim":
                q |= Q(is_active=True)
            if self.request.GET['status'].lower() in "nao":
                q |= Q(is_active=False)

        if 'ativo' in self.request.GET:
            q &= Q(is_active__icontains=self.request.GET['ativo'])

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
