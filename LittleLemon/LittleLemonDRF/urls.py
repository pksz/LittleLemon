from django.urls import path , include
from . import views 
  
urlpatterns = [ 
    path('',include('djoser.urls')),
    path('',include('djoser.urls.authtoken')),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemsView.as_view()),
    path('groups/manager/users', views.ManagerGroupUsers.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerGroupUsers.as_view()),
    path('groups/delivery-crew/users', views.DeliverCrewUsers.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliverCrewUsers.as_view()),
    path('cart/menu-items',views.CartManagement.as_view()),
    path('orders',views.OrderManagement.as_view()),
    path('orders/<int:pk>',views.OrderModify.as_view()),
    

] 