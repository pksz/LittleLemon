from rest_framework import serializers
from . models import Booking,Menu
from django.contrib.auth.models import User
from rest_framework import viewsets

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['url', 'username', 'email', 'groups']

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model=Booking
        fields='__all__'


class MenuItemserializer(serializers.ModelSerializer):

    class Meta:
        model=Menu
        fields='__all__'

