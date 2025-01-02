from django.urls import path
from .views import RestaurantListView , RestaurantDetailView , home


urlpatterns = [
    
    path('', home, name='home'),  
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),

]

