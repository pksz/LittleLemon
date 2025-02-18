
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem

#menu
class MenuItemSerializer(serializers.ModelSerializer):
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = MenuItem
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            'price': {'min_value': 0.0},
        }

#user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'id','email', 'groups']
        extrer_kwargs = {
            'id': {'read_only': True},
            'groups': {'read_only': True},
            'email': {'read_only': True},
        }

#cart handler
class CartSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menuitem=serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    class Meta:
        model=Cart
        fields=['user','menuitem','quantity','unit_price','price']
        extra_kwargs={
            "price":{"read_only":True},
            "quantity":{"min_value": 1},
            "unit_price":{"read_only":True},
        }
        validators=[
            UniqueTogetherValidator(queryset=Cart.objects.all(),
                                    fields=['user','menuitem'],
                                    message="This menu item is already in the cart for this user."
                                )
        ]
    
    def create(self, validated_data):
        user=self.context['request'].user #gets the user from the request
        menu_item=validated_data['menuitem']
        unit_price=menu_item.price      #get the price from menu
        quantity=validated_data['quantity']
        price=unit_price*quantity   #calculate total price

        cart_item,created=Cart.objects.get_or_create(
            user=user,
            menuitem=menu_item,
            quantity= quantity, 
            unit_price= menu_item.price,
            price= menu_item.price * quantity)
            

        return cart_item
    
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:

        model=Order
        fields='__all__'
        extra_kwargs={
            "user":{"read_only":True},
            "total":{"read_only":True},

        }

class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:

        model=OrderItem
        fields='__all__'




       