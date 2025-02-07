from django.db import models

# Create your models here.

class Booking(models.Model):
    ID=models.CharField(max_length=11,null=False,blank=False,primary_key=True)
    name=models.CharField(max_length=255)
    no_of_guests=models.PositiveSmallIntegerField(default=1)
    bookingDate=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.Name


class Menu(models.Model):
    ID=models.CharField(max_length=11,null=False,blank=False,primary_key=True)
    title=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.title

