from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .models import MenuItem,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,UserSerializer,CartSerializer,OrderSerializer,OrderItemSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User,Group
from django_filters.rest_framework import DjangoFilterBackend


#menu item endpoints and menuitem{pk} endpoints
class MenuItemsView(generics.ListCreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'price']  # Fields allowed for filtering
    ordering_fields = ['price', 'featured']   # Fields allowed for ordering
    search_fields = ['title']  # Fields to search for (ensure 'name' exists in MenuItem model)

    #get queryset for filtering
    def get_queryset(self):
        queryset=super().get_queryset()
        
        pk=self.kwargs.get('pk')

        if pk:
            return queryset.filter(pk=pk)
        return queryset
    #get request for menu-items  also for menuitem{pk}
    
    def get(self, request, *args, **kwargs):
        queryset=self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response({"message": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if 'pk'in kwargs:
            serializer = self.get_serializer(queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:  
            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data) 
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    #post request for menu-items
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().post(request, *args, **kwargs)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)
        
    #put request for menu-items
    def put(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().put(request, *args, **kwargs)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)
        
    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().patch(request, *args, **kwargs)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)

    #delete request for menu-items
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            return super().delete(request, *args, **kwargs)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)
        

#user group management endpoint
class ManagerGroupUsers(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            context=super().get(request, *args, **kwargs)
            context.data=UserSerializer(User.objects.filter(groups__name='manager'),many=True).data
            return Response(context.data,status=status.HTTP_200_OK)
        
        else:
             return Response({"message":"You are not authorized to view this page"},status=status.HTTP_403_FORBIDDEN)
        
    #send username through post request body to add a manager
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            username=request.data.get('username')
            user=User.objects.get(username=username)
            manager_group=Group.objects.get(name='manager')
            if user.groups.filter(name='manager').exists():
                 return Response({"message":f"user {username} is alraedy a manager"},status=status.HTTP_400_BAD_REQUEST)
            user.groups.add(manager_group)
            return Response({f"user {user} added to managers"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, *args, **kwargs):        
        if request.user.groups.filter(name='manager').exists(): 
            if 'pk' in kwargs:                
                user=User.objects.get(id=kwargs['pk'])
                username=user.username
                manager_group=Group.objects.get(name='manager')
                if not user.groups.filter(name='manager').exists():
                    return Response({"message":f"user {username} is not a manager"},status=status.HTTP_400_BAD_REQUEST)
                user.groups.remove(manager_group)
                return Response({"user {user} removed from to managers"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)
      

#delivery-Crew management endpoint
class DeliverCrewUsers(generics.ListCreateAPIView,generics.DestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            context=super().get(request, *args, **kwargs)
            context.data=UserSerializer(User.objects.filter(groups__name='Delivery_crew'),many=True).data
            return Response(context.data,status=status.HTTP_200_OK)
        
        else:
             return Response({"message":"You are not authorized to view this page"},status=status.HTTP_403_FORBIDDEN)
        
    #send username through post request body to add as delivery crew
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists():
            username=request.data.get('username')
            user=User.objects.get(username=username)
            delivrey_crew_group=Group.objects.get(name='Delivery_crew')
            if user.groups.filter(name='Delivery_crew').exists():
                    return Response({"message":f"user {username} is alraedy in delivery crew"},status=status.HTTP_400_BAD_REQUEST)
            user.groups.add(delivrey_crew_group)
            return Response({f"user {user} added to managers"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, *args, **kwargs):        
        if request.user.groups.filter(name='manager').exists():
            if 'pk'in kwargs: 
                user=User.objects.get(id=kwargs['pk'])
                username=user.username
                delivery_crew_group=Group.objects.get(name='Delivery_crew')
                if not user.groups.filter(name='Delivery_crew').exists():
                    return Response({"message":f"user {username} is not in delivery Crew"},status=status.HTTP_400_BAD_REQUEST)
                user.groups.remove(delivery_crew_group)
                return Response({"message:"f"user {username} removed from to managers"},status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"You are not authorized to perform this action"},status=status.HTTP_403_FORBIDDEN)


#cart management endpints
class CartManagement(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        context= super().get(request, *args, **kwargs)
        context.data=CartSerializer(Cart.objects.filter(user=request.user),many=True).data
        return Response(context.data,status=status.HTTP_200_OK)
    
    #gets the user through request
    #gets the price and total price by matching queries
    #only needs menuitem id and quantity in api request
    def post(self, request, *args, **kwargs):
        #pass the current user through context
        serializer=CartSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
           cart_item=serializer.save()
           return Response(CartSerializer(cart_item).data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        user=request.user
        #filter by curent user and delete the cart
        deleted,info=Cart.objects.filter(user=user).delete()
        if deleted:
            return Response({"message":"Cart Emptied"},status=status.HTTP_200_OK)
        else:
             return Response({"message":"Cart is already empty"},status=status.HTTP_200_OK)
        

#order managemnet endpoints for get and post
class OrderManagement(generics.ListCreateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        context= super().get(request, *args, **kwargs)
        #MANAGER
        if self.request.user.groups.filter(name="manager").exists():
            context.data=OrderSerializer(Order.objects.all(),many=True).data
            return Response(context.data,status=status.HTTP_200_OK)
        #delivery crew
        elif self.request.user.groups.filter(name="Delivery_crew").exists():
            context.data=OrderSerializer(Order.objects.filter(delivery_crew=request.user),many=True).data
            return Response(context.data,status=status.HTTP_200_OK)
        #customer
        else:
            context.data=OrderSerializer(Order.objects.filter(user=request.user),many=True).data
            return Response(context.data,status=status.HTTP_200_OK)
        
    #create an order for the user
    #Creating order and deleting user cart
    def post(self, request, *args, **kwargs):
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            cart=Cart.objects.filter(user=self.request.user)
            if not cart:
                return Response({"message":"cart is empty"},status=status.HTTP_200_OK)
            
            #calculate total amount
            total_=0
            for item in cart:
                total_=total_+item.price
            #create order
            order=Order.objects.create(user=request.user,total=total_)
            
            #create order items for order
            for item in cart:
                orderitem=OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitem,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price=item.price

                )
            order.save()
            cart.delete()
            return Response({"message":f"Order Created {order.id}"},status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

#order managemnet endpoints for get<pk> update/patch and delete
class OrderModify(generics.RetrieveUpdateDestroyAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    #get the user's order
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            context= super().get(request, *args, **kwargs)
            #get orders for current user
            orders=Order.objects.get(id=kwargs['pk'])
          
            if orders.user!=self.request.user:
                return Response(status=status.HTTP_404_NOT_FOUND)
            context.data=OrderItemSerializer(OrderItem.objects.filter(order=orders.id),many=True).data
            
            return Response(context.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    #customer and manager accessible ,only manager can change stuff in excercise so i removed customer access
    def put(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="manager").exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        #get the order
        try:
            order=Order.objects.get(id=kwargs['pk'])
        except:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=OrderSerializer(order,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
   
    #delicery crew updates the order
    def patch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="Delivery_crew").exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        #get the order
        try:
            order=Order.objects.get(id=kwargs['pk'])
        except:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        allowed_fields={"status"} #only status can be updated here

        #check for allowd fields
        update_data={}
        for key,value in request.data.items():
            if key in allowed_fields:
                update_data[key]=value

        if not update_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer=OrderSerializer(order,data=update_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    #only manager
    def delete(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="manager").exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                order=Order.objects.get(id=kwargs['pk'])
                order.delete()
                return Response({"message":"Order removed"},status=status.HTTP_200_OK)
            except:
                return Response({"message":"Order not found"},status=status.HTTP_200_OK)
