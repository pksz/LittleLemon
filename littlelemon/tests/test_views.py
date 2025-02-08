from django.test import TestCase
from restaurant.models import Booking,Menu
from rest_framework import status
from rest_framework.test import APIClient
class MenuViewTest(TestCase):
    def setUp(self):
        self.item1 = Menu.objects.create(ID=1, title="Pizza", price=7.99, inventory=5)
        self.item2 = Menu.objects.create(ID=2, title="Burger", price=5.99, inventory=3)
        self.item3 = Menu.objects.create(ID=3, title="Pasta", price=6.99, inventory=4)
        return super().setUp()
    
    def test_getall(self):
        response = self.client.get('/restaurant/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Pizza')
        self.assertEqual(response.data[1]['title'], 'Burger')
        self.assertEqual(response.data[2]['title'], 'Pasta')
    