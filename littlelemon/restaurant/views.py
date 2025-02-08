from django.shortcuts import render
from .serializers import BookingSerializer,MenuItemserializer
from . models import Booking,Menu
from rest_framework import generics
from rest_framework import viewsets
# Create your views here.

# def index(request):
#     return render(request,'index.html')

class MenuItemView(generics.ListCreateAPIView):
    queryset=Menu.objects.all()
    serializer_class=MenuItemserializer



class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Menu.objects.all()
    serializer_class=MenuItemserializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer
    