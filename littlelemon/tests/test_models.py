from django.test import TestCase
from restaurant.models import Menu


class MenuTest(TestCase):    
    def test_get_item(self):
        item=Menu.objects.create(ID=1,title="Pizza",price=7.99,inventory=5)
        self.assertEqual(item.__str__(),"Pizza : 7.99")