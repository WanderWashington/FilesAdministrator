from rest_framework import serializers
from .models import User
from .models import Address
from .models import File
from .models import FileHistory
from datetime import date
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from .validators import FileValidator
from django.db import models

class FileSerializer(serializers.ModelSerializer):

	class Meta:
		model = File
		fields = ('file', 'userRelated')

	def create(self, validated_data):
		fileData = File.objects.create(**validated_data)
		if fileData:
			FileHistory.objects.create(user_add= validated_data.get('userRelated'), fileRelativePath= fileData.file.url)

		return fileData




class AddressSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ('zipCode', 'houseNumber', 'nghood',
                  'city', 'houseType', 'state')

class UserSerializer(serializers.ModelSerializer):
	addresses = AddressSerializer(many=False, required=False)

	class Meta:
		model = User
		fields = ('id',  'nome', 'email', 'password', 'is_staff',  'addresses')
		read_only_fields = ['date_joined']

		extra_kwargs = {
			'email': {
				'validators':[UnicodeUsernameValidator()]
			}
		}

	def create(self, validated_data):
		addresses_data = validated_data.pop('addresses')

		user = User.objects.create_user(**validated_data)
		if addresses_data:
			Address.objects.create(user=user, **addresses_data)

		return user


class UserNonAdminSerializer(serializers.ModelSerializer):
	addresses = AddressSerializer(many=False, required=False)

	class Meta:
		model = User
		fields = ('id',  'nome', 'email', 'password', 'addresses')
		read_only_fields = ['date_joined']

		extra_kwargs = {
			'email': {
				'validators':[UnicodeUsernameValidator()]
			}
		}

	def create(self, validated_data):
		addresses_data = validated_data.pop('addresses')
		user = User.objects.create_user(**validated_data)
		if addresses_data:
			Address.objects.create(user=user, **addresses_data)

		return user


class FileHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = FileHistory
		fields = ('__all__')

	# def create(self, validated_data):
 #        endereco_data = validated_data.pop('enderecos')
 #        user = User.objects.create_user(**validated_data)

 #        Endereco.objects.create(usuario=user, **endereco_data[0])


 #        return user