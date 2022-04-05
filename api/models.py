from django.db import models
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.forms import Field
from django.forms import ModelChoiceField
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from .validators import FileValidator
from django.conf import settings


class Pagination(PageNumberPagination):
    page_size_query_param = 'pagination'

    def getPageNumber(self):
        #  total de itens no solicitacao
        qtd = int(self.page.paginator.count)
        # quantidade de itens por pagina
        numero_itens = int(self.get_page_size(self.request))

        pagina_adicional = qtd % numero_itens
        numero_paginas = qtd // numero_itens

        if qtd == 0:
            return "1"

        if numero_itens >= qtd:
            return "1"

        if pagina_adicional > 0:
            return numero_paginas + 1
        else:
            return numero_paginas

    def getPaginatedResponse(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('num_paginas', self.get_numero_de_paginas())
        ]))


# ------- USER -----------------------------------------


class UserManager(BaseUserManager):

    def create_user(self, email, password=None,
                    **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('O email é obrigatório')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='E-mail (Obrigatório para acesso ao sistema)', unique=True)
    nome = models.CharField(verbose_name='Nome', max_length=100)

    is_active = models.BooleanField('ativo', default=True,)
    is_staff = models.BooleanField('administrador', default=False,)
    date_joined = models.DateTimeField('data de cadastro', default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('nome', )



    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome.split(' ')[0]


class Address(models.Model):

    zipCode = models.CharField('ZipCode', max_length=9, null=True)
    houseNumber = models.CharField('Number', max_length=6, null=True)
    nghood = models.CharField('Neighborhood', max_length=50, null=True)
    city = models.CharField('City/Town', max_length=40, null=True)
    houseType = models.CharField('Type', max_length=50, null=True, blank=True)
    state = models.CharField('State', max_length=2, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.PROTECT,
                                related_name='user', unique=True)


class File(models.Model):
   file = models.FileField(null=True, blank=True, upload_to='static', validators=[FileValidator()])
   userRelated = models.ForeignKey(User, null=False, on_delete=models.PROTECT, unique=False)


class FileHistory(models.Model):
    fileRelativePath = models.TextField("filePath")
    date_add = models.DateTimeField(auto_now_add=True, editable=False)
    user_add = models.ForeignKey(User, null = False, on_delete=models.PROTECT, unique=False)


class GetAddressesMixin(object):
    def get_addresses(self):
        return Address.objects.filter(
            content_type=get_content_type_for_model(self),
            object_id=self.pk
        )

    def get_addresses_json(self):
        # import pdb;pdb.set_trace()
        qs = Address.objects.filter(
            content_type=get_content_type_for_model(self),
            object_id=self.pk).values()
        dados = json.dumps(str(qs[0]))
        # dados = json.dumps(qs)
        # # v  = json.loads(qs)
        # json = json.dumps(data)

        return dados


